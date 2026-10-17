"""
ui_components.py - Premium Three.js 3D WebGL Hardware Space & Futuristic Cyberpunk Glassmorphism for SpecSense AI.
"""

def render_3d_electronics_background():
    """
    Renders an interactive Three.js 3D WebGL hardware universe directly into the Streamlit parent document.
    Spans the entire screen with dual cybernetic grids (floor & ceiling), floating 3D microchips on left and right flanks,
    and a full-viewport quantum data particle constellation.
    """
    import streamlit.components.v1 as components

    bg_component_code = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {
        const parentDoc = window.parent.document;
        if (!parentDoc) return;

        // Prevent duplicate background canvases on Streamlit reruns
        if (parentDoc.getElementById('spec-sense-3d-bg-canvas')) return;

        // Inject container into parent document body
        const container = parentDoc.createElement('div');
        container.id = 'spec-sense-3d-bg-container';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100vw';
        container.style.height = '100vh';
        container.style.zIndex = '0';
        container.style.pointerEvents = 'none';
        container.style.overflow = 'hidden';
        container.style.background = 'radial-gradient(ellipse at 50% 50%, #0c1527 0%, #050813 60%, #020307 100%)';
        parentDoc.body.prepend(container);

        // Canvas for Three.js
        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'spec-sense-3d-bg-canvas';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.display = 'block';
        container.appendChild(canvas);

        // Ensure Streamlit container transparency & styling
        const style = parentDoc.createElement('style');
        style.id = 'spec-sense-transparency-override';
        style.innerHTML = `
            html, body {
                background: transparent !important;
            }
            [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stBottom"], .stApp {
                background-color: transparent !important;
                background: transparent !important;
            }
            [data-testid="stAppViewBlockContainer"] {
                position: relative;
                z-index: 10;
            }
        `;
        parentDoc.head.appendChild(style);

        // Verify Three.js availability
        if (typeof THREE === 'undefined') {
            console.warn("Three.js CDN not ready, falling back to procedural 2D Canvas");
            run2DFallback(canvas, parentDoc);
            return;
        }

        try {
            // Three.js Scene Setup
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x050813, 0.0012);

            const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 3500);
            camera.position.set(0, 0, 520);

            const renderer = new THREE.WebGLRenderer({
                canvas: canvas,
                alpha: true,
                antialias: true
            });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            // Lighting
            const ambientLight = new THREE.AmbientLight(0x00f2fe, 0.85);
            scene.add(ambientLight);

            const cyanLight = new THREE.PointLight(0x00f2fe, 3.0, 1200);
            cyanLight.position.set(-300, 200, 300);
            scene.add(cyanLight);

            const purpleLight = new THREE.PointLight(0x8338ec, 3.2, 1200);
            purpleLight.position.set(300, -200, 300);
            scene.add(purpleLight);

            const emeraldLight = new THREE.PointLight(0x10b981, 2.0, 800);
            emeraldLight.position.set(0, 0, 200);
            scene.add(emeraldLight);

            // Full-Screen Cybernetic Dual Grids (Floor & Ceiling)
            const gridFloor = new THREE.GridHelper(3200, 80, 0x00f2fe, 0x111e38);
            gridFloor.position.y = -360;
            scene.add(gridFloor);

            const gridCeiling = new THREE.GridHelper(3200, 80, 0x8338ec, 0x111e38);
            gridCeiling.position.y = 360;
            scene.add(gridCeiling);

            // 3D Microchip Builder
            function createMicrochip(label, subtext, colorHex, x, y, z, size) {
                const group = new THREE.Group();

                // Silicon Die / Ceramic Body
                const bodyGeo = new THREE.BoxGeometry(size, size * 0.72, 9);
                const bodyMat = new THREE.MeshPhysicalMaterial({
                    color: 0x090f1c,
                    metalness: 0.9,
                    roughness: 0.2,
                    clearcoat: 1.0,
                    clearcoatRoughness: 0.1
                });
                const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
                group.add(bodyMesh);

                // Metallic Heat-Spreader Plate
                const plateGeo = new THREE.BoxGeometry(size * 0.76, size * 0.52, 10.5);
                const plateMat = new THREE.MeshStandardMaterial({
                    color: 0x152238,
                    metalness: 0.95,
                    roughness: 0.15
                });
                const plateMesh = new THREE.Mesh(plateGeo, plateMat);
                group.add(plateMesh);

                // Neon Edge Wireframe
                const edgesGeo = new THREE.EdgesGeometry(bodyGeo);
                const edgesMat = new THREE.LineBasicMaterial({ color: colorHex, linewidth: 2 });
                const wireframe = new THREE.LineSegments(edgesGeo, edgesMat);
                group.add(wireframe);

                // Gold Contact Pins
                const pinMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.95, roughness: 0.15 });
                const pinGeo = new THREE.BoxGeometry(2.5, 7, 4.5);
                const pinCount = 7;
                for (let i = 0; i < pinCount; i++) {
                    const offset = -size / 2 + (size / (pinCount - 1)) * i;
                    const pTop = new THREE.Mesh(pinGeo, pinMat);
                    pTop.position.set(offset, size * 0.36 + 3.5, 0);
                    group.add(pTop);
                    const pBot = new THREE.Mesh(pinGeo, pinMat);
                    pBot.position.set(offset, -size * 0.36 - 3.5, 0);
                    group.add(pBot);
                }

                // Laser-Etched Text Label
                const textCanvas = document.createElement('canvas');
                textCanvas.width = 256;
                textCanvas.height = 128;
                const ctx = textCanvas.getContext('2d');
                ctx.fillStyle = '#0f172a';
                ctx.fillRect(0, 0, 256, 128);
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 24px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(label, 128, 54);
                ctx.fillStyle = '#' + colorHex.toString(16).padStart(6, '0');
                ctx.font = '15px monospace';
                ctx.fillText(subtext, 128, 88);

                const textTex = new THREE.CanvasTexture(textCanvas);
                const labelGeo = new THREE.PlaneGeometry(size * 0.72, size * 0.36);
                const labelMat = new THREE.MeshBasicMaterial({ map: textTex, transparent: true });
                const labelMesh = new THREE.Mesh(labelGeo, labelMat);
                labelMesh.position.z = 5.6;
                group.add(labelMesh);

                group.position.set(x, y, z);
                group.userData = {
                    rotSpeedX: (Math.random() - 0.5) * 0.009,
                    rotSpeedY: (Math.random() - 0.5) * 0.009,
                    rotSpeedZ: (Math.random() - 0.5) * 0.005,
                    floatBaseY: y,
                    floatOffset: Math.random() * Math.PI * 2
                };
                return group;
            }

            // Distribute 3D Chips Across the ENTIRE Viewport (Left, Right, Depth)
            const chips = [
                // Left Flank (Top, Mid, Bottom)
                createMicrochip('APPLE M3', '16-CORE NPU', 0x00f2fe, -450, 190, -90, 85),
                createMicrochip('SNAPDRAGON', '8 GEN 3 4NM', 0xff0055, -480, -30, -110, 85),
                createMicrochip('GEN4 NVMe', '7000 MB/s SSD', 0xffbe0b, -430, -250, -80, 80),

                // Right Flank (Top, Mid, Bottom)
                createMicrochip('RTX 4070', '140W TGP GDDR6', 0x00ff88, 450, 190, -90, 90),
                createMicrochip('LPDDR5X', '6400 MT/s RAM', 0x8338ec, 480, -30, -120, 85),
                createMicrochip('AI NPU CORE', '45 TOPS MATRIX', 0x38bdf8, 430, -250, -80, 80),

                // Central Deep Core
                createMicrochip('SPECSENSE AI', 'NEURAL ENGINE', 0x00f2fe, 0, 0, -380, 130)
            ];
            chips.forEach(c => scene.add(c));

            // Full-Viewport Quantum Data Particle Cloud (1,200 Particles)
            const particleCount = 1200;
            const particleGeo = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const colors = new Float32Array(particleCount * 3);

            const colorOptions = [
                new THREE.Color(0x00f2fe),
                new THREE.Color(0x8338ec),
                new THREE.Color(0x38bdf8),
                new THREE.Color(0x10b981),
                new THREE.Color(0xffd700)
            ];

            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = (Math.random() - 0.5) * 2200;
                positions[i * 3 + 1] = (Math.random() - 0.5) * 1600;
                positions[i * 3 + 2] = (Math.random() - 0.5) * 1400 - 100;

                const col = colorOptions[Math.floor(Math.random() * colorOptions.length)];
                colors[i * 3] = col.r;
                colors[i * 3 + 1] = col.g;
                colors[i * 3 + 2] = col.b;
            }

            particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const particleMat = new THREE.PointsMaterial({
                size: 3.2,
                vertexColors: true,
                transparent: true,
                opacity: 0.75
            });
            const particleSystem = new THREE.Points(particleGeo, particleMat);
            scene.add(particleSystem);

            // Mouse parallax tracker
            let targetMouseX = 0, targetMouseY = 0;
            let currentMouseX = 0, currentMouseY = 0;

            parentDoc.addEventListener('mousemove', (e) => {
                targetMouseX = (e.clientX - window.innerWidth / 2) * 0.15;
                targetMouseY = (e.clientY - window.innerHeight / 2) * 0.10;
            });

            // Resize handling
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            // Main Animation Loop
            let clock = new THREE.Clock();

            function animate() {
                requestAnimationFrame(animate);

                const elapsedTime = clock.getElapsedTime();

                // Smooth mouse interpolation
                currentMouseX += (targetMouseX - currentMouseX) * 0.04;
                currentMouseY += (targetMouseY - currentMouseY) * 0.04;

                camera.position.x = currentMouseX;
                camera.position.y = -currentMouseY;
                camera.lookAt(0, 0, 0);

                // Rotate & Float Chips
                chips.forEach(chip => {
                    chip.rotation.x += chip.userData.rotSpeedX;
                    chip.rotation.y += chip.userData.rotSpeedY;
                    chip.rotation.z += chip.userData.rotSpeedZ;
                    chip.position.y = chip.userData.floatBaseY + Math.sin(elapsedTime * 1.5 + chip.userData.floatOffset) * 14;
                });

                // Animate Dual Cyber Grids (Endless movement)
                gridFloor.position.z = (elapsedTime * 50) % 40;
                gridCeiling.position.z = (elapsedTime * 50) % 40;

                // Animate Particle Matrix
                particleSystem.rotation.y = elapsedTime * 0.018;
                particleSystem.rotation.x = elapsedTime * 0.009;

                renderer.render(scene, camera);
            }

            animate();
            console.log("⚡ Full-Screen 3D Hardware Space active!");

        } catch (err) {
            console.error("Three.js initialization error:", err);
            run2DFallback(canvas, parentDoc);
        }

        function run2DFallback(cvs, doc) {
            const ctx = cvs.getContext('2d');
            let w = cvs.width = window.innerWidth;
            let h = cvs.height = window.innerHeight;
            window.addEventListener('resize', () => {
                w = cvs.width = window.innerWidth;
                h = cvs.height = window.innerHeight;
            });
            function draw2D() {
                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#060913';
                ctx.fillRect(0, 0, w, h);
                requestAnimationFrame(draw2D);
            }
            draw2D();
        }
    })();
    </script>
    """
    components.html(bg_component_code, height=0)


def get_custom_css() -> str:
    """
    Returns custom CSS for the fixed top-left branding navbar, cyberpunk glassmorphism,
    and responsive telemetry cards.
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Body and Streamlit Container Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: transparent !important;
        background: transparent !important;
        font-family: 'Outfit', sans-serif !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        display: none !important; /* Hide default Streamlit top bar */
    }

    /* Add space for fixed top navbar */
    .main .block-container {
        padding-top: 80px !important;
        max-width: 1280px !important;
    }

    /* Fixed Top-Left Branding Navbar */
    .fixed-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: rgba(6, 10, 22, 0.88);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-bottom: 1px solid rgba(0, 242, 254, 0.22);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        z-index: 999999;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
    }

    .brand-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(131, 56, 236, 0.2));
        border: 1px solid rgba(0, 242, 254, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }

    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 1.45rem;
        background: linear-gradient(135deg, #ffffff 40%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }

    .brand-badge {
        background: rgba(0, 242, 254, 0.12);
        border: 1px solid rgba(0, 242, 254, 0.4);
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        color: #00f2fe;
        letter-spacing: 0.08em;
    }

    /* Subtitle banner under fixed header */
    .page-hero-banner {
        margin: 10px 0 24px 0;
        text-align: left;
    }

    .page-hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 6px;
    }

    .page-hero-desc {
        color: #94a3b8;
        font-size: 1.02rem;
        max-width: 820px;
        line-height: 1.55;
    }

    /* Native Streamlit Bordered Container as Glass Card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(12, 19, 36, 0.78) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(0, 242, 254, 0.22) !important;
        border-radius: 18px !important;
        padding: 10px !important;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.8), 0 0 25px -4px rgba(0, 242, 254, 0.15) !important;
        margin-bottom: 20px !important;
    }

    /* Glassmorphic Output Cards */
    .glass-card {
        background: rgba(12, 19, 36, 0.82) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.8), 0 0 25px -4px rgba(0, 242, 254, 0.18) !important;
    }

    /* Risk Level Banners */
    .risk-banner {
        border-radius: 16px;
        padding: 18px 24px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 22px;
        font-family: 'Space Grotesk', sans-serif;
    }

    .risk-badge-group {
        display: flex;
        align-items: center;
        gap: 14px;
        flex-shrink: 0;
        min-width: 220px;
    }

    .risk-micro-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        opacity: 0.8;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 3px;
        white-space: nowrap;
    }

    .risk-level-title {
        font-size: 1.4rem;
        font-weight: 800;
        white-space: nowrap;
        letter-spacing: 0.02em;
    }

    .risk-lifespan-card {
        flex: 1 1 320px;
        background: rgba(0, 0, 0, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 18px;
        text-align: left;
    }

    .risk-lifespan-value {
        font-size: 1.02rem;
        font-weight: 600;
        line-height: 1.45;
        word-break: break-word;
    }

    .risk-low {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.6);
        color: #10b981;
        box-shadow: 0 0 30px -4px rgba(16, 185, 129, 0.4);
    }

    .risk-moderate {
        background: rgba(245, 158, 11, 0.16);
        border: 1px solid rgba(245, 158, 11, 0.6);
        color: #f59e0b;
        box-shadow: 0 0 30px -4px rgba(245, 158, 11, 0.4);
    }

    .risk-high {
        background: rgba(239, 68, 68, 0.16);
        border: 1px solid rgba(239, 68, 68, 0.7);
        color: #ef4444;
        box-shadow: 0 0 35px -3px rgba(239, 68, 68, 0.45);
    }

    .risk-out-of-scope {
        background: rgba(139, 92, 246, 0.16);
        border: 1px solid rgba(139, 92, 246, 0.7);
        color: #a78bfa;
        box-shadow: 0 0 35px -3px rgba(139, 92, 246, 0.45);
    }

    /* Jargon Busters */
    .analogy-card {
        background: rgba(20, 30, 56, 0.7);
        border-left: 4px solid #00f2fe;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    .analogy-label {
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        color: #00f2fe;
        letter-spacing: 0.08em;
        margin-bottom: 3px;
    }

    .analogy-text {
        font-size: 0.96rem;
        color: #f1f5f9;
        font-style: italic;
    }

    /* Missing Specs Badges */
    .missing-tag {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #fca5a5;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
        margin: 4px 6px 6px 0;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* Persona Metric Cards */
    .persona-card {
        background: rgba(16, 26, 48, 0.8);
        border: 1px solid rgba(0, 242, 254, 0.22);
        border-radius: 14px;
        padding: 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .score-circle {
        font-size: 2.2rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
    }

    .pill-advantage {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
        font-size: 0.82rem;
        border-radius: 6px;
        padding: 4px 8px;
        margin-bottom: 4px;
    }

    .pill-bottleneck {
        background: rgba(239, 68, 68, 0.16);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        font-size: 0.82rem;
        border-radius: 6px;
        padding: 4px 8px;
        margin-bottom: 4px;
    }

    /* Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #8338ec 100%) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.02rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        box-shadow: 0 8px 25px -4px rgba(0, 242, 254, 0.5) !important;
        transition: all 0.25s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 14px 35px -2px rgba(0, 242, 254, 0.8) !important;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(10, 16, 32, 0.85) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 18px rgba(0, 242, 254, 0.35) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(10, 16, 30, 0.7);
        padding: 6px 10px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 242, 254, 0.16) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.45) !important;
    }

    /* Responsive Dynamic Media Queries for Window Resizing */
    @media (max-width: 992px) {
        div[data-testid="column"] {
            min-width: calc(50% - 0.75rem) !important;
            flex: 1 1 calc(50% - 0.75rem) !important;
            margin-bottom: 12px !important;
        }
        .risk-banner {
            flex-direction: column !important;
            align-items: stretch !important;
        }
        .risk-lifespan-card {
            width: 100% !important;
        }
    }

    @media (max-width: 640px) {
        div[data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 10px !important;
        }
        .main .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
            padding-top: 75px !important;
        }
        .brand-title {
            font-size: 1.2rem !important;
        }
        .brand-badge {
            display: none !important;
        }
    }

    footer {visibility: hidden;}
    </style>
    """


def get_fixed_navbar_html() -> str:
    """
    Returns the fixed top navbar HTML pinned permanently to the top-left of the viewport.
    """
    return """
    <div class="fixed-navbar">
        <div class="brand-section">
            <div class="brand-icon-box">⚡</div>
            <div class="brand-title">SpecSense AI</div>
            <span class="brand-badge">HARDWARE INTELLIGENCE</span>
        </div>
    </div>
    """
