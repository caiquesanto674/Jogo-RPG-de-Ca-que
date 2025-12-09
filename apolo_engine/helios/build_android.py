"""
APOLO ENGINE – MÓDULO HÉLIOS
PARTE 9 – Build Android / Gerador Automático de APK

Este módulo cria automaticamente:
- Ambiente de build Android
- Estrutura compatible com APK
- Empacotamento do motor APOLO ENGINE
- Geração do APK final
"""

import os
import shutil
from datetime import datetime
from ..chronos.backup import CronosBackup
from ..atlas.structure_guard import AtlasStructureGuard

class HeliosAPKBuilder:
    def __init__(self, project_root: str = ".", output: str = "./dist"):
        self.root = project_root
        self.output = output
        self.build_dir = "./.build_apk"

        if not os.path.exists(self.output):
            os.makedirs(self.output)

        self.cronos = CronosBackup(root=self.root)
        self.atlas = AtlasStructureGuard(root="apolo_engine")

    # ----------------------------------------------------------------------
    # PREPARAR ESTRUTURA DO PROJETO PARA ANDROID
    # ----------------------------------------------------------------------
    def prepare_android_structure(self):
        print("[HÉLIOS] Preparando estrutura Android...")

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

        # Copiar o motor inteiro
        shutil.copytree("apolo_engine", f"{self.build_dir}/apolo_engine")

        # Copiar assets
        if os.path.exists("assets"):
            shutil.copytree("assets", f"{self.build_dir}/assets")

        # Empacotar entrada do jogo
        shutil.copy("main.py", f"{self.build_dir}/main.py")

        # Garantir integridade estrutural
        self.atlas.ensure_structure()

    # ----------------------------------------------------------------------
    # GERAR ARQUIVOS NECESSÁRIOS PARA COMPILAÇÃO ANDROID
    # ----------------------------------------------------------------------
    def generate_android_manifest(self):
        manifest = f"""
<?xml version="1.0" encoding="utf-8"?>
<manifest package="com.apoloengine.rpg"
    xmlns:android="http://schemas.android.com/apk/res/android">

    <application android:label="RPG Apolo Engine">
        <activity android:name="MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
        """
        with open(f"{self.build_dir}/AndroidManifest.xml", "w") as f:
            f.write(manifest)

    # ----------------------------------------------------------------------
    # COMPILAR / GERAR O APK
    # ----------------------------------------------------------------------
    def build_apk(self):
        print("[HÉLIOS] Criando backup antes do build...")
        snapshot = self.cronos.create_snapshot()

        print("[HÉLIOS] Iniciando processo de build Android...")

        # Comando simbólico para fins de estrutura do projeto
        apk_name = f"rpg_apolo_engine_{datetime.now().strftime('%Y%m%d_%H%M')}.apk"
        final_path = os.path.join(self.output, apk_name)

        # Em um projeto real usaríamos buildozer/kivy/p4a
        # Aqui criamos o arquivo como representação do empacotamento
        with open(final_path, "w") as f:
            f.write("APK SIMBÓLICO – Conteúdo gerado pelo sistema HÉLIOS.")

        print(f"[HÉLIOS] APK gerado: {final_path}")
        return final_path
