"""
Assinador automátio de APK (versão simulada).
"""

class HeliosSigner:
    def sign(self, apk_path: str):
        print(f"[HÉLIOS] Assinando o APK: {apk_path}")
        return apk_path + ".signed.apk"
