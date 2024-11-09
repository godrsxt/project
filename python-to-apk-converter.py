import os
import sys
import shutil
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pkg_resources
import re

class PyToApkConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python to APK Converter")
        self.geometry("600x400")
        
        # Initialize variables
        self.python_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.app_name = tk.StringVar()
        self.package_name = tk.StringVar()
        self.icon_path = tk.StringVar()
        
        # Common error patterns and solutions
        self.error_solutions = {
            "Cython": self.install_package_solution("Cython"),
            "virtualenv": self.install_package_solution("virtualenv"),
            "Cannot find command git": self.install_git,
            "Command failed: pkg-config": self.install_system_package("pkg-config"),
            "java": self.install_system_package("default-jdk"),
            "SDK": self.handle_sdk_error,
            "NDK": self.handle_ndk_error,
            "JAVA_HOME": self.set_java_home,
            "build-tools": self.install_build_tools,
        }
        
        self.setup_ui()

    def check_git_installation(self):
        """Check if git is installed and accessible"""
        try:
            subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def install_git(self):
        """Install git based on the operating system"""
        self.log_message("Installing Git...")
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'git'])
            elif sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['brew', 'install', 'git'])
            elif sys.platform.startswith('win'):
                # For Windows, we'll guide the user to install Git manually
                messagebox.showinfo(
                    "Git Installation Required",
                    "Please install Git from https://git-scm.com/download/win"
                )
                return False
            return True
        except Exception as e:
            self.log_message(f"Error installing Git: {str(e)}")
            return False

    def install_dependencies(self):
        # Check and install Git first
        if not self.check_git_installation():
            self.log_message("Git not found. Installing Git...")
            if not self.install_git():
                raise Exception("Failed to install Git. Please install it manually.")
        else:
            self.log_message("Git is already installed.")

        # Install required packages
        required_packages = ['buildozer', 'kivy', 'cython']
        for package in required_packages:
            try:
                pkg_resources.require(package)
            except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                self.log_message(f"Installing {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        self.log_message("Dependencies installed")

    # [Previous methods remain unchanged]
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Python file selection
        ttk.Label(main_frame, text="Python File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.python_file, width=50).grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_python_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        # App icon selection
        ttk.Label(main_frame, text="App Icon:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.icon_path, width=50).grid(row=2, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_icon).grid(row=2, column=2, padx=5, pady=5)
        
        # App name
        ttk.Label(main_frame, text="App Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.app_name, width=50).grid(row=3, column=1, pady=5)
        
        # Package name
        ttk.Label(main_frame, text="Package Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.package_name, width=50).grid(row=4, column=1, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Convert button
        ttk.Button(main_frame, text="Convert to APK", command=self.convert_to_apk).grid(row=6, column=0, columnspan=3, pady=10)
        
        # Log area
        self.log_text = tk.Text(main_frame, height=10, width=60)
        self.log_text.grid(row=7, column=0, columnspan=3, pady=10)

    def browse_python_file(self):
        filename = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if filename:
            self.python_file.set(filename)
            # Auto-set app name from file name
            suggested_name = Path(filename).stem.capitalize()
            self.app_name.set(suggested_name)
            # Auto-set package name
            suggested_package = f"com.{suggested_name.lower()}"
            self.package_name.set(suggested_package)
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            
    def browse_icon(self):
        filename = filedialog.askopenfilename(
            title="Select App Icon",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        if filename:
            self.icon_path.set(filename)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.update_idletasks()
        
    def install_package_solution(self, package_name):
        def solution():
            self.log_message(f"Installing {package_name}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package_name])
            return True
        return solution
        
    def install_system_package(self, package_name):
        def solution():
            if sys.platform.startswith('linux'):
                self.log_message(f"Installing {package_name}...")
                subprocess.run(['sudo', 'apt-get', 'install', '-y', package_name])
                return True
            else:
                self.log_message(f"Please install {package_name} manually on your system")
                return False
        return solution
        
    def handle_sdk_error(self):
        self.log_message("Downloading Android SDK...")
        subprocess.run(['buildozer', 'android', 'update'])
        return True
        
    def handle_ndk_error(self):
        self.log_message("Downloading Android NDK...")
        subprocess.run(['buildozer', 'android', 'update'])
        return True
        
    def set_java_home(self):
        if sys.platform.startswith('linux'):
            java_path = subprocess.check_output(['update-alternatives', '--query', 'java']).decode()
            java_home = re.search(r'Value: (.+)/bin/java', java_path).group(1)
            os.environ['JAVA_HOME'] = java_home
            return True
        else:
            self.log_message("Please set JAVA_HOME environment variable manually")
            return False
            
    def install_build_tools(self):
        self.log_message("Installing Android build tools...")
        subprocess.run(['buildozer', 'android', 'update'])
        return True
        
    def handle_error(self, error_output):
        for error_pattern, solution in self.error_solutions.items():
            if error_pattern.lower() in error_output.lower():
                self.log_message(f"Attempting to fix {error_pattern} error...")
                if solution():
                    return True
        return False
        
    def convert_to_apk(self):
        if not all([self.python_file.get(), self.output_dir.get(), 
                   self.app_name.get(), self.package_name.get()]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        try:
            self.progress['value'] = 0
            self.log_message("Starting conversion process...")
            
            # Create buildozer.spec file
            self.create_buildozer_spec()
            self.progress['value'] = 20
            
            # Install dependencies
            self.log_message("Installing dependencies...")
            self.install_dependencies()
            self.progress['value'] = 40
            
            # Build APK with error handling
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    self.log_message(f"Building APK... (Attempt {retry_count + 1}/{max_retries})")
                    process = subprocess.Popen(['buildozer', 'android', 'debug'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True)
                    
                    # Monitor the build process
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            self.log_message(output.strip())
                            
                    if process.returncode == 0:
                        break
                    else:
                        error_output = process.stderr.read()
                        if not self.handle_error(error_output):
                            retry_count += 1
                            if retry_count == max_retries:
                                raise Exception("Maximum retry attempts reached")
                        
                except Exception as e:
                    self.log_message(f"Error during build: {str(e)}")
                    retry_count += 1
                    if retry_count == max_retries:
                        raise
                        
            self.progress['value'] = 80
            
            # Move APK to output directory
            self.move_apk()
            self.progress['value'] = 100
            
            self.log_message("Conversion completed successfully!")
            messagebox.showinfo("Success", "APK file created successfully!")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            
    def create_buildozer_spec(self):
        spec_content = f"""[app]
title = {self.app_name.get()}
package.name = {self.package_name.get()}
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET
android.api = 29
android.minapi = 21
android.sdk = 24
android.ndk = 19b
android.private_storage = True
"""
        
        # Add icon configuration if provided
        if self.icon_path.get():
            icon_path = self.icon_path.get()
            spec_content += f"icon.filename = {icon_path}\n"
            # Copy icon to project directory
            icon_dest = Path(Path(self.python_file.get()).parent / Path(icon_path).name)
            shutil.copy2(icon_path, icon_dest)
            
        with open('buildozer.spec', 'w') as f:
            f.write(spec_content)
        self.log_message("Created buildozer.spec file")
            
    def move_apk(self):
        # Move the generated APK to output directory
        apk_path = next(Path('bin').glob('*.apk'))
        output_path = Path(self.output_dir.get()) / f"{self.app_name.get()}.apk"
        shutil.move(str(apk_path), str(output_path))
        self.log_message(f"APK moved to: {output_path}")

if __name__ == '__main__':
    app = PyToApkConverter()
    app.mainloop()