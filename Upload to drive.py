import json
import requests
headers = {"Authorization": "Bearer ya29.a0AfH6SMDIRxrjF_z06LmuQ2bbOz7DM5yHMquUsTUo00OzQ1cqrqtkCsrM-07_WfXH5naQ3cZ-UgMBdp0GIHPafJeiiI2siQSDDvtpsXKFL61DIYWOQeAVrMKF_W98W07DT2ixeu_7GZeC6ZhmsT_kMGfK0xjh"}
para = {
    "name": "test1.wav",
    "parents": ["16Xqs2DNb9VGj6d9QpJZ79xW17NjWZsMd"]
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./test1.wav", "rb")
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)
print(r.text)

