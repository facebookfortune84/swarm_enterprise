import os
import shutil
import uuid
import zipfile
from datetime import datetime

class SwarmReplicator:
    def __init__(self, source_dir="/app", output_base="/app/output"):
        self.source_dir = source_dir
        self.output_base = output_base
        # Files to EXCLUDE from the sale (personal secrets)
        self.ignore_list = [
            '__pycache__', '.git', 'node_modules', 
            'memory_data', 'nginx_data', '.env', 
            'output', '.docker'
        ]

    def create_saleable_package(self):
        """Creates a clean, portable version of the entire swarm company."""
        package_id = f"Company_In_A_Box_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:4]}"
        export_path = os.path.join(self.output_base, package_id)
        
        print(f"Replicator: Initiating build for {package_id}...")

        try:
            # 1. Copy the core codebase
            if os.path.exists(export_path):
                shutil.rmtree(export_path)
            
            shutil.copytree(
                self.source_dir, 
                export_path, 
                ignore=shutil.ignore_patterns(*self.ignore_list)
            )

            # 2. Generate a Template .env for the buyer
            self._generate_template_env(export_path)

            # 3. Create the Windows Bootstrap Script
            self._create_bootstrap_script(export_path)

            # 4. Zip the entire company
            zip_file = f"{export_path}.zip"
            self._make_zip(export_path, zip_file)

            # 5. Cleanup the temporary folder
            shutil.rmtree(export_path)

            print(f"Replicator: Success! Package ready at {zip_file}")
            return zip_file

        except Exception as e:
            print(f"Replicator Error: {e}")
            return None

    def _generate_template_env(self, target_path):
        """Creates a blank environment file for the buyer."""
        template = (
            "# SWARM ENTERPRISE - BUYER CONFIGURATION\n"
            "CLOUDFLARE_TUNNEL_TOKEN=PASTE_YOUR_TOKEN_HERE\n"
            "OLLAMA_URL=http://[YOUR_LAPTOP_IP]:11434\n"
            "STRIPE_SECRET_KEY=PASTE_YOUR_STRIPE_KEY_HERE\n"
            "DOMAIN=your-new-domain.com\n"
            "DB_PASSWORD=SetSecurePassword123!\n"
        )
        with open(os.path.join(target_path, ".env.example"), "w") as f:
            f.write(template)

    def _create_bootstrap_script(self, target_path):
        """Creates a one-click startup for Windows users."""
        script = (
            "@echo off\n"
            "echo ===========================================\n"
            "echo   SWARM ENTERPRISE: COMPANY IN A BOX\n"
            "echo ===========================================\n"
            "echo Step 1: Checking for Docker...\n"
            "docker --version >nul 2>&1\n"
            "if %errorLevel% neq 0 (\n"
            "    echo ERROR: Docker is not installed. Please install Docker Desktop.\n"
            "    pause\n"
            "    exit\n"
            ")\n"
            "echo Step 2: Launching Infrastructure...\n"
            "docker compose up -d --build\n"
            "echo SUCCESS: Your Company is live at http://localhost\n"
            "pause\n"
        )
        with open(os.path.join(target_path, "START_COMPANY.bat"), "w") as f:
            f.write(script)

    def _make_zip(self, source, destination):
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), source)
                    )

if __name__ == "__main__":
    rep = SwarmReplicator()
    rep.create_saleable_package()
