import json
import re

content = """aaa{
   '@context":"https://schema.org',
   "@type":"Product","name":"Samsung Galaxy Tab A 8 SM-T290 32 GB 8" Tablet",
   "image":"https://n11scdn.akamaized.net/a1/450/elektronik/ipad-ve-tablet/samsung-galaxy-tab-a-8-sm-t290-32-gb-8-tablet__1464918373225445.jpg",
   "description":"Samsung Galaxy Tab A 8 SM-T290 32 GB 8" Tablet en iyi özellikleri ve gerçek kullanıcı yorumları en ucuz fiyatlarla n11.com"da. Kampanyalı ve indirimli fiyatlarla satın al.",
   "brand":"Samsung",
   "offers":{
	  "@type":"AggregateOffer",
	  "priceCurrency":"TRY",
	  "lowPrice":"1029.17",
	  "offerCount":"8"
   },
   "aggregateRating":{
	  "@type":"AggregateRating",
	  "ratingValue":"5",
	  "reviewCount":"59"
   },
   "review":[
	  {
		 "@type":"Review",
		 "name":"n11.com üyesi",
		 "reviewBody":"Evet beğendim. Seçtiğim ürün geldi.",
		 "reviewRating":{
			"@type":"Rating",
			"ratingValue":"5"
		 },
		 "datePublished":"2021-04-28",
		 "author":{
			"@type":"Person",
			"name":"n11.com üyesi"
		 },
		 "publisher":{
			"@type":"Organization",
			"name":"n11.com üyesi"
		 }
	  }
   ]
} bbb"""

def break_line(content):
	content = content.replace('\'','"')
	content = re.sub(r'(",)', r'\1\n', content)
	content = re.sub(r'({)', r'\1\n', content)
	content = re.sub(r'(})', r'\1\n', content)
	content = re.sub(r'(\[)', r'\1\n', content)
	content_v2 = re.sub(r'(])', r'\1\n', content)
	return content_v2

def create_new_content(content_v2):
	new_content = ''
	for line in content_v2.split('\n'):
		line_double_quote_idx_list = []
		for idx, char in enumerate(line):
			if char == '"':
				line_double_quote_idx_list.append(idx)
		new_line = replace_double_quote_as_single_quote(line, line_double_quote_idx_list)
		new_content += new_line
	
	return new_content

def replace_double_quote_as_single_quote(line, line_double_quote_idx_list):
	if line.count('"') <= 2:
		return f"{line}\n"
	del line_double_quote_idx_list[0:3]
	del line_double_quote_idx_list[-1]
	if not line_double_quote_idx_list:
		return f"{line}\n"
	else:
		new_line = ''
		for idx, char in enumerate(line):
			if idx in line_double_quote_idx_list:
				new_line += '\''
			else:
				new_line += char
		return f"{new_line}\n"

def extract_only_json_from_string(content, start_value, end_value):
	content = content.replace('\n','').replace('\t','')
	pattern = re.compile(f'{start_value}(.*?){end_value}')
	matches = pattern.findall(content)
	return matches[0]

def regulate_json(content, start_value="", end_value=""):
	content = extract_only_json_from_string(content, start_value, end_value)
	content_v2 = break_line(content)
	new_content = create_new_content(content_v2)
	return json.loads(new_content)

print(regulate_json(content,"aaa"," bbb"))


