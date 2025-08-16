#!/usr/bin/env python3
"""
clean_property_data.py

Improved cleaning script for property_details.json.

Usage:
    python clean_property_data.py                 # reads ./property_details.json -> ./property_details_cleaned.json
    python clean_property_data.py input.json out.json
"""

import re
import json
import sys
import argparse
from typing import Union, List, Dict, Any

# ---------- Helpers ----------
NUMBER_RE = re.compile(r'([0-9]+(?:[.,][0-9]+)?)')
PRICE_PER_SQ_RE = re.compile(r'₹\s*([0-9,]+(?:\.[0-9]+)?)\s*/\s*sq', re.IGNORECASE)
AREA_RE = re.compile(r'([0-9]+(?:[.,][0-9]+)?)\s*(sqft|ftk|sq\.?ft|sq)', re.IGNORECASE)
INT_RE = re.compile(r'\d+')

def _to_float_safe(x):
    try:
        if x is None or x == "":
            return None
        if isinstance(x, (int, float)):
            return float(x)
        s = str(x).strip()
        s = s.replace(",", "")
        return float(s)
    except Exception:
        return None

def _extract_first_number(s: str):
    if s is None or s == "":
        return None
    s = str(s)
    # find first reasonable number
    m = NUMBER_RE.search(s.replace(",", ""))
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except:
        return None

def _parse_price_str(s: str):
    """Parse price or per-sqft from text; returns numeric value (INR) or per-sqft number depending on content."""
    if s is None or s == "":
        return None
    s = str(s).strip()
    s_n = s.replace(",", "").lower()

    # Try ₹.../sqft pattern (returns per-sqft)
    per_sq_match = PRICE_PER_SQ_RE.search(s)
    if per_sq_match:
        try:
            return float(per_sq_match.group(1).replace(",", ""))
        except:
            return None

    # Big units: cr, lakh
    if 'cr' in s_n:
        try:
            val = float(re.sub(r'[^0-9.]', '', s_n.replace('cr', '')))
            return val * 1e7
        except:
            return None
    if 'lakh' in s_n or 'lac' in s_n:
        try:
            val = float(re.sub(r'[^0-9.]', '', s_n.replace('lakh', '').replace('lac', '')))
            return val * 1e5
        except:
            return None

    # fallback: first number
    return _extract_first_number(s)

def _parse_floor_info(floor_str: str):
    """Return (current_floor:int or None, total_floors:int or None) from strings like '15(Out of 33 Floors)'."""
    if not floor_str:
        return None, None
    s = str(floor_str)
    nums = re.findall(r'\d+', s)
    if not nums:
        return None, None
    if len(nums) == 1:
        return int(nums[0]), None
    return int(nums[0]), int(nums[1])

def _parse_parking(parking_str: str):
    if not parking_str:
        return None, None
    s = str(parking_str)
    count = _extract_first_number(s)
    typ = None
    m = re.search(r'(covered|open|basement|visitor|reserved|stilt)', s, re.IGNORECASE)
    if m:
        typ = m.group(1).capitalize()
    return (int(count) if count is not None else None), typ

def _extract_area_and_ppsq(super_built_raw: str):
    """
    From a noisy 'Super Built-up Area' string, try to get (area_sqft, price_per_sqft).
    Example input: "2220...₹9,369/sqft" -> returns (2220.0, 9369.0)
    """
    if not super_built_raw:
        return None, None
    text = str(super_built_raw)
    # price per sqft
    ppsq = None
    mpp = PRICE_PER_SQ_RE.search(text)
    if mpp:
        try:
            ppsq = float(mpp.group(1).replace(",", ""))
        except:
            ppsq = None
    # area
    area = None
    marea = AREA_RE.search(text)
    if marea:
        try:
            area = float(marea.group(1).replace(",", ""))
        except:
            area = None
    # fallback: first big integer (>=3 digits)
    if area is None:
        bigs = re.findall(r'\d{3,}', text.replace(',', ''))
        if bigs:
            try:
                area = float(bigs[0])
            except:
                area = None
    return area, ppsq

def _get_first_key(record: Dict[str, Any], candidates: List[str]):
    """Return first found value for any key in candidates (case-insensitive)."""
    if not isinstance(record, dict):
        return None
    lower_map = {k.lower(): v for k, v in record.items()}
    for cand in candidates:
        if cand is None:
            continue
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None

def _collect_photos(record: Dict[str, Any]) -> (List[str], List[str]): # type: ignore
    """Collect property photos and locality photos from all possible source keys and dedupe."""
    photo_keys = [
        "Project Photos", "ProjectPhotos", "project_photos", "project photos",
        "property photos", "property_photos", "Property Photos", "PropertyPhotos"
    ]
    locality_keys = ["Locality Photos", "LocalityPhotos", "locality_photos", "locality photos"]
    photos = []
    for k in photo_keys:
        v = _get_first_key(record, [k])
        if v:
            if isinstance(v, list):
                photos.extend(v)
            elif isinstance(v, str):
                photos.append(v)
    # also check for lower-cased variants used earlier like 'property photos' etc.
    locality_photos = []
    for k in locality_keys:
        v = _get_first_key(record, [k])
        if v:
            if isinstance(v, list):
                locality_photos.extend(v)
            elif isinstance(v, str):
                locality_photos.append(v)
    # dedupe preserving order
    def dedupe(seq):
        seen = set()
        out = []
        for x in seq:
            if not x or x in seen:
                continue
            seen.add(x)
            out.append(x)
        return out
    return dedupe(photos), dedupe(locality_photos)

# ---------- Main cleaning function ----------
def clean_property_data(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    single_input = False
    if isinstance(data, dict):
        # handle possibility of nested list: { "somekey": [ ... ] } -> treat as list if top val is list of dicts
        # but primary expected input: dict as a single record
        data_list = [data]
        single_input = True
    elif isinstance(data, list):
        # sometimes input is [[...]] (double bracket). Unwrap one level if detected
        if len(data) == 1 and isinstance(data[0], list):
            data_list = data[0]
        else:
            data_list = data
    else:
        raise ValueError("Input must be a dict or list of dicts.")

    cleaned_list = []
    for rec in data_list:
        r = dict(rec) if isinstance(rec, dict) else {}
        cleaned = {}

        # canonical property id (try many variants)
        property_id = _get_first_key(r, ["Property ID", "PropertyId", "property_id", "property id", "id"])
        if property_id is None:
            # fallback to Name + lat + lon if available
            name_f = _get_first_key(r, ["Name", "name"])
            lat_f = _get_first_key(r, ["Latitude", "latitude", "lat"])
            lon_f = _get_first_key(r, ["Longitude", "longitude", "lon"])
            if name_f and lat_f is not None and lon_f is not None:
                property_id = f"{name_f}__{lat_f}__{lon_f}"
            else:
                # create a fallback unique id from index (not ideal, but avoids skipping)
                # we'll still include original raw data so you can inspect
                property_id = None

        # basic fields
        cleaned['property_id'] = str(property_id) if property_id is not None else None
        cleaned['name'] = _get_first_key(r, ["Name", "name", "Name "]) or None
        cleaned['bhk'] = None
        bhk_val = _get_first_key(r, ["BHK", "bhk", "Rooms", "rooms"])
        if bhk_val is None and cleaned['name']:
            # try to extract from name like '3 BHK'
            m = re.search(r'(\d+)\s*bhk', str(cleaned['name']), re.IGNORECASE)
            if m:
                bhk_val = m.group(1)
        if bhk_val is not None:
            cleaned['bhk'] = int(_to_float_safe(bhk_val)) if _to_float_safe(bhk_val) is not None else None

        cleaned['property_type'] = _get_first_key(r, ["type", "property_type", "Property Type", "Type"]) or None
        cleaned['developer'] = _get_first_key(r, ["Developer", "developer"]) or None
        cleaned['project'] = _get_first_key(r, ["Project", "project"]) or None

        # Floor info: try several keys and parse if needed
        floor_current = _get_first_key(r, ["Floor (current)", "Floor_current", "floor_current", "Floor (current)"])
        floor_total = _get_first_key(r, ["Floor (total)", "Floor_total", "floor_total", "Floor (total)"])
        floor_field = _get_first_key(r, ["Floor", "Floor Size", "FloorSize"])
        if (floor_current is None or floor_total is None) and floor_field:
            cur, tot = _parse_floor_info(floor_field)
            if floor_current is None:
                floor_current = cur
            if floor_total is None:
                floor_total = tot
        cleaned['floor_current'] = int(_to_float_safe(floor_current)) if _to_float_safe(floor_current) is not None else None
        cleaned['floor_total'] = int(_to_float_safe(floor_total)) if _to_float_safe(floor_total) is not None else None

        cleaned['transaction_type'] = _get_first_key(r, ["Transaction type", "transaction_type", "Transaction Type"]) or None
        cleaned['facing'] = _get_first_key(r, ["Facing", "facing"]) or None
        cleaned['furnished_status'] = _get_first_key(r, ["Furnishing", "Furnished Status", "FurnishedStatus", "Furnished Status", "Furnished"]) or None
        cleaned['ownership_type'] = _get_first_key(r, ["Type of Ownership", "ownership_type", "Type Of Ownership"]) or None
        cleaned['description'] = _get_first_key(r, ["Description", "description"]) or None

        # location
        cleaned['latitude'] = _to_float_safe(_get_first_key(r, ["Latitude", "latitude", "lat"]))
        cleaned['longitude'] = _to_float_safe(_get_first_key(r, ["Longitude", "longitude", "lon"]))
        cleaned['locality'] = _get_first_key(r, ["Locality", "locality", "Locality "]) or None
        cleaned['region'] = _get_first_key(r, ["Region", "region"]) or None
        cleaned['property_url'] = _get_first_key(r, ["Property URL", "property_url", "Property Url", "PropertyUrl"]) or None

        # Areas & prices
        # Super built-up area may contain both area and ppsq
        super_built_raw = _get_first_key(r, ["Super Built-up Area", "super_built_up_area", "Super Builtup Area", "Super Built-up"])
        sb_area, sb_ppsq = _extract_area_and_ppsq(super_built_raw)
        cleaned['super_built_up_area'] = _to_float_safe(sb_area)

        # Total area, floor size
        total_area = _get_first_key(r, ["Total Area (sqft)", "Total Area", "total_area", "Floor Size", "FloorSize"])
        if total_area is None and sb_area is not None:
            total_area = sb_area
        cleaned['total_area_sqft'] = _to_float_safe(total_area)

        # Carpet area
        carpet_area = _get_first_key(r, ["Carpet Area (sqft)", "Carpet Area", "carpet_area"])
        cleaned['carpet_area_sqft'] = _to_float_safe(carpet_area)

        # Price Per Sqft (prefer explicit; else use sb_ppsq extracted)
        ppsq_raw = _get_first_key(r, ["Price Per Sqft", "PricePerSqft", "price_per_sqft"])
        cleaned['price_per_sqft'] = _to_float_safe(ppsq_raw) or _to_float_safe(sb_ppsq)

        # Price (INR)
        price_in = _get_first_key(r, ["Price (INR)", "Price", "price_in_inr", "price"])
        cleaned['price_in_inr'] = _to_float_safe(_parse_price_str(price_in) if isinstance(price_in, str) else price_in) if price_in is not None else (_to_float_safe(price_in) if price_in is not None else None)

        # If price_per_sqft still missing and we have price and total_area, compute it
        if cleaned.get('price_per_sqft') is None and cleaned.get('price_in_inr') is not None and cleaned.get('total_area_sqft') is not None:
            try:
                if cleaned['total_area_sqft'] > 0:
                    cleaned['price_per_sqft'] = float(cleaned['price_in_inr']) / float(cleaned['total_area_sqft'])
            except Exception:
                cleaned['price_per_sqft'] = None

        # Property yield
        property_yield = _get_first_key(r, ["Property Yield (%)", "Property Yield", "property_yield"])
        cleaned['property_yield'] = _to_float_safe(property_yield)

        # Status
        cleaned['status'] = _get_first_key(r, ["Status", "status"]) or None

        # Parking
        parking_count_val = _get_first_key(r, ["parking_count", "Car parking", "Car Parking", "parkingCount"])
        parking_type_val = None
        # sometimes "4 Covered"
        if parking_count_val is None:
            combined_parking = _get_first_key(r, ["Car parking", "Car Parking"])
            if combined_parking:
                parking_count_val, parking_type_val = _parse_parking(combined_parking)
        else:
            # if parking count present as number string, try to parse count and type
            if isinstance(parking_count_val, str) and re.search(r'[a-zA-Z]', parking_count_val):
                parking_count_val, parking_type_val = _parse_parking(parking_count_val)
        if parking_type_val is None:
            parking_type_val = _get_first_key(r, ["parking_type", "Parking Type", "parking_type"]) or None
        cleaned['parking_count'] = int(_to_float_safe(parking_count_val)) if _to_float_safe(parking_count_val) is not None else None
        cleaned['parking_type'] = parking_type_val

        # Photos (merged & deduped)
        photos, locality_photos = _collect_photos(r)
        cleaned['photos'] = photos
        cleaned['locality_photos'] = locality_photos

        # Locality Ratings normalize
        lr_raw = _get_first_key(r, ["Locality Ratings", "Locality_Ratings", "locality_ratings", "locality ratings"])
        if isinstance(lr_raw, dict):
            cleaned['locality_ratings'] = {
                'connectivity': _to_float_safe(lr_raw.get('connectivity')),
                'safety': _to_float_safe(lr_raw.get('safety')),
                'traffic': _to_float_safe(lr_raw.get('traffic')),
                'environment': _to_float_safe(lr_raw.get('environment')),
                'market': _to_float_safe(lr_raw.get('market')),
                'area_description': lr_raw.get('area_description') or lr_raw.get('area description') or None
            }
        else:
            cleaned['locality_ratings'] = {
                'connectivity': None, 'safety': None, 'traffic': None,
                'environment': None, 'market': None, 'area_description': None
            }

        # Historical Price (Locality) normalize (keep as dict month->float)
        hist_raw = _get_first_key(r, ["Historical Price (Locality)", "Historical Price", "historical_prices"])
        if isinstance(hist_raw, dict):
            new_hist = {}
            for k, v in hist_raw.items():
                new_hist[str(k)] = _to_float_safe(v)
            cleaned['historical_price_locality'] = new_hist
        else:
            cleaned['historical_price_locality'] = {}

        # Lifts normalized to int (if present)
        lifts = _get_first_key(r, ["Lifts", "lifts"])
        cleaned['lifts'] = int(_to_float_safe(lifts)) if _to_float_safe(lifts) is not None else None

        # Normalize textual fields capitalization where appropriate
        if cleaned.get('furnished_status'):
            cleaned['furnished_status'] = str(cleaned['furnished_status']).strip().title()
        if cleaned.get('status'):
            cleaned['status'] = str(cleaned['status']).strip().title()

        # Keep original raw for inspection if needed (optional)
        cleaned['_raw'] = r

        # final housekeeping: ensure canonical numeric types
        for k in ['super_built_up_area', 'total_area_sqft', 'carpet_area_sqft', 'price_per_sqft', 'price_in_inr', 'property_yield', 'latitude', 'longitude']:
            if cleaned.get(k) is not None:
                cleaned[k] = _to_float_safe(cleaned[k])

        cleaned_list.append(cleaned)

    return cleaned_list[0] if single_input else cleaned_list

# ---------- Command-line entry ----------
def main():
    parser = argparse.ArgumentParser(description="Clean property JSON file")
    parser.add_argument('input', nargs='?', default='./property_details.json', help='Input JSON file (default: ./property_details.json)')
    parser.add_argument('output', nargs='?', default='./property_details_cleaned.json', help='Output cleaned JSON file (default: ./property_details_cleaned.json)')
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not open/parse input file {args.input}: {e}", file=sys.stderr)
        sys.exit(2)

    cleaned = clean_property_data(payload)

    try:
        with open(args.output, 'w', encoding='utf-8') as fo:
            json.dump(cleaned, fo, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write output file {args.output}: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"[OK] Cleaned data written to {args.output} (records: {len(cleaned) if isinstance(cleaned, list) else 1})")

if __name__ == '__main__':
    main()
