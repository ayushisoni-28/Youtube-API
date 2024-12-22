from googleapiclient.discovery import build

api_key='API KEy'

youtube=build('youtube','v3',developerKey=api_key)

request=youtube.channels().list(part='statistics',forUsername='tseries')

response=request.execute()
print(response)