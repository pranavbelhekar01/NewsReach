import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents"]

# The ID of a sample document.
DOCUMENT_ID = "1_p81ZioFt0QIiS3SrDtlbjMKZmQQVKxhISkA4iLnHRo"


def get_text_and_image_info(document, document_id):
  """Extracts text content and image information from a Google Doc."""
  
  body = document.get('body', {})
  content = body.get('content', [])

  text = ""
  image_info = []
  for element in content:
    if 'paragraph' in element:
      for paragraph in element['paragraph']['elements']:
        if 'textRun' in paragraph:
          text += paragraph['textRun'].get('content', '')
    elif 'imageProperties' in element:
      image_properties = element['embeddedObject']['imageProperties']
      print('Image Properties', image_properties)
      width = image_properties.get('width', {})
      height = image_properties.get('height', {})
      image_info.append({
        'width': width.get('magnitude'),
        'height': height.get('magnitude'),
        'unit': width.get('unit')  
      })
    else:
      print('something not found!!!')

  return text, image_info


def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          r"C:\Job\Textify\DocumentAnalysis\Document Analysis\credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("docs", "v1", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    text_content = get_text_and_image_info(document, DOCUMENT_ID)
    print(f'TEXT::::::::::\n {text_content}')

    
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()