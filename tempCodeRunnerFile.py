credential_scope = f'{date_stamp}/{REGION}/{SERVICE}/aws4_request'
string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'
signing_key = get_signature_key(SECRET_KEY, date_stamp, REGION, SERVICE)
signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
headers = {
    'Content-Encoding': 'utf-8',
    'Content-Type': content_type,
    'Host': HOST,
    'X-Amz-Date': amz_date,
    'X-Amz-Target': amz_target,
    'Authorization': f'{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
}
response = requests.post(ENDPOINT, data=content, headers=headers)
if response.status_code == 200:
    return response.json()
else:
    print(f"Request failed (status {response.status_code}): {response.text}")
    return None
if __name__ == "__main__":
keyword = "iPhone"
print(f"Searching for products in Electronics category with keyword: {keyword}")
results = search_items(keyword)
if results:
    print(json.dumps(results, indent=4))  # Pretty print the JSON response
else:
    print("No products found.")
