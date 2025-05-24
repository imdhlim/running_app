import requests
import json
import os
from datetime import datetime
from urllib.parse import quote
import traceback
import xml.etree.ElementTree as ET

def fetch_all_region_data():
    try:
        print("=== 전국 법정동 데이터 수집 시작 ===")
        base_url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
        service_key = "qzsWuuVIqRgrwOqIFsr3lf6EP1mg9VuGgKQ5NMprFVkNBGt8LDOc1wNbhasB3vMsTj2R6jmpRS/GIGWNnx29MQ=="
        url = f"{base_url}?ServiceKey={quote(service_key)}"
        num_of_rows = 1000
        page_no = 1
        all_items = []

        while True:
            print(f"요청: page {page_no}")
            params = {
                "pageNo": str(page_no),
                "numOfRows": str(num_of_rows),
                "flag": "Y"
            }
            response = requests.get(url, params=params)
            print(f"응답 코드: {response.status_code}")
            print(f"응답 일부: {response.text[:200]}...")
            response.raise_for_status()

            root = ET.fromstring(response.text)
            items = root.findall('.//row')
            if not items:
                print("더 이상 데이터 없음, 종료")
                break
            def row_to_dict(row):
                return {child.tag: child.text for child in row}
            all_items.extend([row_to_dict(item) for item in items])
            total_count_elem = root.find('.//totalCount')
            total_count = int(total_count_elem.text) if total_count_elem is not None else len(all_items)
            print(f"페이지 {page_no} 수집, 누적 {len(all_items)}/{total_count}")
            if len(all_items) >= total_count:
                break
            page_no += 1

        os.makedirs("assets/data", exist_ok=True)
        current_date = datetime.now().strftime("%Y%m%d")
        output_file = f"assets/data/region_{current_date}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        print(f"전국 데이터 저장 완료: {output_file}")
    except Exception as e:
        print("오류 발생!")
        traceback.print_exc()

if __name__ == "__main__":
    fetch_all_region_data() 