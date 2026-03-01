import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 1. Configuración de Seguridad
# Usamos el permiso completo para evitar errores de acceso
SCOPES = ['https://www.googleapis.com/auth/youtube']
# SUSTITUYE AQUÍ: Pon el ID que encontraste (ejemplo: 'UC1234567890')
CHANNEL_ID_PAPA = 'UCVlJ1ViIjXtlCXNFYPq4vcw' 

def get_authenticated_service():
    creds = None
    # Buscamos el token de sesión guardado
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Lee tu archivo credentials.json desde la carpeta config
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def test_direct_access():
    youtube = get_authenticated_service()
    try:
        print(f"🔎 Verificando acceso al canal: {CHANNEL_ID_PAPA}...")
        
        # Llamada directa al ID del canal de noticias
        request = youtube.channels().list(
            part="snippet,statistics",
            id=CHANNEL_ID_PAPA
        )
        response = request.execute()
        
        if response.get('items'):
            canal_nombre = response['items'][0]['snippet']['title']
            print(f"🚀 ¡CONECTADO DIRECTAMENTE!")
            print(f"📺 Trabajando sobre: {canal_nombre}")
        else:
            print("⚠️ El ID es correcto, pero tu cuenta no tiene permisos sobre él.")
            
    except Exception as e:
        print(f"❌ Error de acceso: {e}")

if __name__ == "__main__":
    test_direct_access()