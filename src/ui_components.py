"""
ui_components.py - Premium Three.js 3D WebGL Hardware Space & Futuristic Cyberpunk Glassmorphism for SpecSense AI.
"""

def render_3d_electronics_background():
    """
    Renders an interactive Three.js 3D WebGL hardware universe directly into the Streamlit parent document.
    Spans the entire screen with dual cybernetic grids (floor & ceiling), floating 3D microchips,
    glowing geometric crystals, and a full-viewport quantum data particle constellation with mouse parallax.
    """
    import streamlit.components.v1 as components

    bg_component_code = """
    <script>
    (function() {
        const parentDoc = window.parent.document;
        if (!parentDoc) return;

        // Ensure Three.js script is loaded in the parent document head
        let threeScript = parentDoc.getElementById('spec-sense-three-cdn');
        if (!threeScript) {
            threeScript = parentDoc.createElement('script');
            threeScript.id = 'spec-sense-three-cdn';
            threeScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
            parentDoc.head.appendChild(threeScript);
        }

        // Prevent duplicate background canvases on Streamlit reruns
        let container = parentDoc.getElementById('spec-sense-3d-bg-container');
        if (!container) {
            container = parentDoc.createElement('div');
            container.id = 'spec-sense-3d-bg-container';
            container.style.position = 'fixed';
            container.style.top = '0';
            container.style.left = '0';
            container.style.width = '100vw';
            container.style.height = '100vh';
            container.style.zIndex = '0';
            container.style.pointerEvents = 'none';
            container.style.overflow = 'hidden';
            container.style.background = 'radial-gradient(circle at 50% 35%, #0d172e 0%, #060b17 65%, #020409 100%)';
            parentDoc.body.prepend(container);

            const canvas = parentDoc.createElement('canvas');
            canvas.id = 'spec-sense-3d-bg-canvas';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.display = 'block';
            container.appendChild(canvas);
        }

        // Inject transparency overrides into parent document
        let styleOverride = parentDoc.getElementById('spec-sense-transparency-override');
        if (!styleOverride) {
            styleOverride = parentDoc.createElement('style');
            styleOverride.id = 'spec-sense-transparency-override';
            styleOverride.innerHTML = `
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
            parentDoc.head.appendChild(styleOverride);
        }

        const canvas = parentDoc.getElementById('spec-sense-3d-bg-canvas');
        if (!canvas) return;

        // If WebGL is already running on this canvas, don't re-initialize
        if (canvas.dataset.initialized === 'true') return;

        // Poll for Three.js readiness (handles network latency gracefully)
        let attempts = 0;
        const checkThree = setInterval(() => {
            attempts++;
            const T = window.parent.THREE || (typeof THREE !== 'undefined' ? THREE : null);
            if (T) {
                clearInterval(checkThree);
                initThreeScene(T, canvas, parentDoc);
            } else if (attempts > 50) {
                clearInterval(checkThree);
                console.warn("Three.js load timed out, falling back to 2D animated cyber canvas");
                run2DAnimatedFallback(canvas, parentDoc);
            }
        }, 50);

        function initThreeScene(THREE, cvs, doc) {
            try {
                cvs.dataset.initialized = 'true';
                const win = doc.defaultView || window.parent || window;
                const getW = () => win.innerWidth || doc.documentElement.clientWidth || 1920;
                const getH = () => win.innerHeight || doc.documentElement.clientHeight || 1080;

                const scene = new THREE.Scene();
                scene.fog = new THREE.FogExp2(0x060b17, 0.0011);

                const camera = new THREE.PerspectiveCamera(55, getW() / getH(), 1, 3500);
                camera.position.set(0, 0, 520);

                const renderer = new THREE.WebGLRenderer({
                    canvas: cvs,
                    alpha: true,
                    antialias: true
                });
                renderer.setSize(getW(), getH());
                renderer.setPixelRatio(Math.min(win.devicePixelRatio || 1, 2));

                // Lights
                const ambientLight = new THREE.AmbientLight(0x00f2fe, 0.95);
                scene.add(ambientLight);

                const cyanLight = new THREE.PointLight(0x00f2fe, 3.8, 1400);
                cyanLight.position.set(-350, 220, 320);
                scene.add(cyanLight);

                const purpleLight = new THREE.PointLight(0x8338ec, 3.8, 1400);
                purpleLight.position.set(350, -220, 320);
                scene.add(purpleLight);

                const emeraldLight = new THREE.PointLight(0x10b981, 2.5, 950);
                emeraldLight.position.set(0, 0, 220);
                scene.add(emeraldLight);

                // Dual Infinite Cyber Grids (Floor & Ceiling)
                const gridFloor = new THREE.GridHelper(3800, 95, 0x00f2fe, 0x11213f);
                gridFloor.position.y = -340;
                scene.add(gridFloor);

                const gridCeiling = new THREE.GridHelper(3800, 95, 0x8338ec, 0x11213f);
                gridCeiling.position.y = 340;
                scene.add(gridCeiling);

                // 3D Microchip Builder
                function createMicrochip(label, subtext, colorHex, x, y, z, size) {
                    const group = new THREE.Group();

                    // Silicon Body
                    const bodyGeo = new THREE.BoxGeometry(size, size * 0.72, 9);
                    const bodyMat = new THREE.MeshPhysicalMaterial({
                        color: 0x0a1224,
                        metalness: 0.9,
                        roughness: 0.2,
                        clearcoat: 1.0,
                        clearcoatRoughness: 0.1
                    });
                    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
                    group.add(bodyMesh);

                    // Heat Spreader Plate
                    const plateGeo = new THREE.BoxGeometry(size * 0.76, size * 0.52, 10.5);
                    const plateMat = new THREE.MeshStandardMaterial({
                        color: 0x162645,
                        metalness: 0.95,
                        roughness: 0.15
                    });
                    const plateMesh = new THREE.Mesh(plateGeo, plateMat);
                    group.add(plateMesh);

                    // Neon Wireframe Edges
                    const edgesGeo = new THREE.EdgesGeometry(bodyGeo);
                    const edgesMat = new THREE.LineBasicMaterial({ color: colorHex, linewidth: 2 });
                    const wireframe = new THREE.LineSegments(edgesGeo, edgesMat);
                    group.add(wireframe);

                    // Dual Pin Rows
                    const pinGeo = new THREE.BoxGeometry(size * 0.07, 7, 3);
                    const pinMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.2 });
                    const pinCount = 6;
                    const spacing = (size * 0.8) / (pinCount - 1);
                    for (let i = 0; i < pinCount; i++) {
                        const offset = -size * 0.4 + i * spacing;
                        const pTop = new THREE.Mesh(pinGeo, pinMat);
                        pTop.position.set(offset, size * 0.36 + 3.5, 0);
                        group.add(pTop);
                        const pBot = new THREE.Mesh(pinGeo, pinMat);
                        pBot.position.set(offset, -size * 0.36 - 3.5, 0);
                        group.add(pBot);
                    }

                    // Canvas Label Texture
                    const textCanvas = document.createElement('canvas');
                    textCanvas.width = 256;
                    textCanvas.height = 128;
                    const ctx = textCanvas.getContext('2d');
                    ctx.fillStyle = '#0a1224';
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

                // Microchips Array
                const chips = [
                    createMicrochip('APPLE M3', '16-CORE NPU', 0x00f2fe, -480, 180, -90, 85),
                    createMicrochip('SNAPDRAGON', '8 GEN 3 4NM', 0xff0055, -500, -30, -110, 85),
                    createMicrochip('GEN4 NVMe', '7000 MB/s SSD', 0xffbe0b, -440, -240, -80, 80),
                    createMicrochip('RTX 4070', '140W TGP GDDR6', 0x00ff88, 480, 180, -90, 90),
                    createMicrochip('LPDDR5X', '6400 MT/s RAM', 0x8338ec, 500, -30, -120, 85),
                    createMicrochip('AI NPU CORE', '45 TOPS MATRIX', 0x38bdf8, 440, -240, -80, 80),
                    createMicrochip('SPECSENSE AI', 'HARDWARE ENGINE', 0x00f2fe, 0, 0, -360, 130)
                ];
                chips.forEach(c => scene.add(c));

                // Floating Geometric Crystals (Icosahedrons & Octahedrons)
                const crystals = [];
                const crystalColors = [0x00f2fe, 0x8338ec, 0x10b981, 0xff007f];
                for (let i = 0; i < 8; i++) {
                    const geo = i % 2 === 0 ? new THREE.IcosahedronGeometry(22, 0) : new THREE.OctahedronGeometry(24, 0);
                    const mat = new THREE.MeshStandardMaterial({
                        color: 0x0a1428,
                        metalness: 0.9,
                        roughness: 0.15,
                        wireframe: false
                    });
                    const crystal = new THREE.Mesh(geo, mat);

                    const wireGeo = new THREE.WireframeGeometry(geo);
                    const wireMat = new THREE.LineBasicMaterial({
                        color: crystalColors[i % crystalColors.length],
                        linewidth: 2
                    });
                    const wire = new THREE.LineSegments(wireGeo, wireMat);
                    crystal.add(wire);

                    const x = (i < 4 ? -1 : 1) * (300 + Math.random() * 260);
                    const y = (Math.random() - 0.5) * 500;
                    const z = (Math.random() - 0.5) * 300 - 80;
                    crystal.position.set(x, y, z);
                    crystal.userData = {
                        rotX: (Math.random() - 0.5) * 0.015,
                        rotY: (Math.random() - 0.5) * 0.015,
                        floatSpeed: 0.8 + Math.random() * 0.8,
                        floatBaseY: y
                    };
                    crystals.push(crystal);
                    scene.add(crystal);
                }

                // Quantum Constellation Particle Field (1,200 Nodes)
                const particleCount = 1200;
                const particleGeo = new THREE.BufferGeometry();
                const positions = new Float32Array(particleCount * 3);
                const colors = new Float32Array(particleCount * 3);

                const colorPalette = [
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

                    const col = colorPalette[Math.floor(Math.random() * colorPalette.length)];
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

                // Mouse Parallax Tracker
                let targetMouseX = 0, targetMouseY = 0;
                let currentMouseX = 0, currentMouseY = 0;

                doc.addEventListener('mousemove', (e) => {
                    targetMouseX = (e.clientX - getW() / 2) * 0.16;
                    targetMouseY = (e.clientY - getH() / 2) * 0.11;
                });

                // Window Resize Listener
                win.addEventListener('resize', () => {
                    const w = getW();
                    const h = getH();
                    camera.aspect = w / h;
                    camera.updateProjectionMatrix();
                    renderer.setSize(w, h);
                });

                // Animation Loop
                let clock = new THREE.Clock();

                function animate() {
                    requestAnimationFrame(animate);

                    const elapsedTime = clock.getElapsedTime();

                    // Camera mouse damping
                    currentMouseX += (targetMouseX - currentMouseX) * 0.045;
                    currentMouseY += (targetMouseY - currentMouseY) * 0.045;

                    camera.position.x = currentMouseX;
                    camera.position.y = -currentMouseY;
                    camera.lookAt(0, 0, 0);

                    // Float & Rotate Chips
                    chips.forEach(chip => {
                        chip.rotation.x += chip.userData.rotSpeedX;
                        chip.rotation.y += chip.userData.rotSpeedY;
                        chip.rotation.z += chip.userData.rotSpeedZ;
                        chip.position.y = chip.userData.floatBaseY + Math.sin(elapsedTime * 1.5 + chip.userData.floatOffset) * 14;
                    });

                    // Float & Rotate Crystals
                    crystals.forEach(cr => {
                        cr.rotation.x += cr.userData.rotX;
                        cr.rotation.y += cr.userData.rotY;
                        cr.position.y = cr.userData.floatBaseY + Math.cos(elapsedTime * cr.userData.floatSpeed) * 12;
                    });

                    // Moving Grids
                    gridFloor.position.z = (elapsedTime * 48) % 40;
                    gridCeiling.position.z = (elapsedTime * 48) % 40;

                    // Particle System Drift
                    particleSystem.rotation.y = elapsedTime * 0.016;
                    particleSystem.rotation.x = elapsedTime * 0.008;

                    renderer.render(scene, camera);
                }

                animate();
                console.log("⚡ SpecSense 3D WebGL Space Initialized Successfully!");

            } catch (err) {
                console.error("Three.js setup error:", err);
                run2DAnimatedFallback(cvs, doc);
            }
        }

        // High-Performance Animated 2D Procedural Fallback
        function run2DAnimatedFallback(cvs, doc) {
            const win = doc.defaultView || window.parent || window;
            const getW = () => win.innerWidth || doc.documentElement.clientWidth || 1920;
            const getH = () => win.innerHeight || doc.documentElement.clientHeight || 1080;

            const ctx = cvs.getContext('2d');
            let w = cvs.width = getW();
            let h = cvs.height = getH();
            win.addEventListener('resize', () => {
                w = cvs.width = getW();
                h = cvs.height = getH();
            });

            const nodes = [];
            for (let i = 0; i < 90; i++) {
                nodes.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    vx: (Math.random() - 0.5) * 0.8,
                    vy: (Math.random() - 0.5) * 0.8,
                    r: Math.random() * 2.2 + 1,
                    color: i % 2 === 0 ? '#00f2fe' : '#8338ec'
                });
            }

            function draw2D() {
                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#060b17';
                ctx.fillRect(0, 0, w, h);

                // Draw moving connection lines
                ctx.lineWidth = 0.5;
                for (let i = 0; i < nodes.length; i++) {
                    const n = nodes[i];
                    n.x += n.vx;
                    n.y += n.vy;
                    if (n.x < 0 || n.x > w) n.vx *= -1;
                    if (n.y < 0 || n.y > h) n.vy *= -1;

                    ctx.beginPath();
                    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                    ctx.fillStyle = n.color;
                    ctx.shadowColor = n.color;
                    ctx.shadowBlur = 8;
                    ctx.fill();

                    for (let j = i + 1; j < nodes.length; j++) {
                        const m = nodes[j];
                        const dist = Math.hypot(n.x - m.x, n.y - m.y);
                        if (dist < 110) {
                            ctx.beginPath();
                            ctx.moveTo(n.x, n.y);
                            ctx.lineTo(m.x, m.y);
                            ctx.strokeStyle = `rgba(0, 242, 254, ${1 - dist / 110})`;
                            ctx.stroke();
                        }
                    }
                }
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
    Returns modern custom CSS for the fixed top-left branding navbar, cyberpunk glassmorphism,
    fluid responsive typography, and refined card sizing.
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Body and Streamlit Container Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: transparent !important;
        background: transparent !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        display: none !important;
    }

    /* Fixed top navbar offset & container padding */
    .main .block-container {
        padding-top: 86px !important;
        padding-bottom: 60px !important;
        max-width: 1260px !important;
    }

    /* Fixed Top-Left Branding Navbar */
    .fixed-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 66px;
        background: rgba(6, 11, 24, 0.88);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-bottom: 1px solid rgba(0, 242, 254, 0.22);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
        z-index: 999999;
        box-shadow: 0 6px 30px rgba(0, 0, 0, 0.7);
    }

    .brand-section {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.22), rgba(131, 56, 236, 0.22));
        border: 1px solid rgba(0, 242, 254, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 0 16px rgba(0, 242, 254, 0.4);
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

    .nav-status-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.76rem;
        font-family: 'JetBrains Mono', monospace;
        color: #34d399;
        font-weight: 600;
        letter-spacing: 0.06em;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulseDot 2s infinite ease-in-out;
    }

    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Hero Banner */
    .page-hero-banner {
        margin: 6px 0 24px 0;
        text-align: left;
    }

    .page-hero-title {
        font-size: clamp(1.8rem, 3.2vw, 2.5rem);
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #ffffff 30%, #00f2fe 75%, #8338ec 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }

    .page-hero-desc {
        color: #94a3b8;
        font-size: clamp(0.96rem, 1.4vw, 1.12rem);
        max-width: 860px;
        line-height: 1.6;
    }

    /* Native Streamlit Bordered Container as Cyber Glass Card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(10, 16, 32, 0.76) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(0, 242, 254, 0.22) !important;
        border-radius: 18px !important;
        padding: 14px 18px !important;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.75), 0 0 25px -4px rgba(0, 242, 254, 0.14) !important;
        margin-bottom: 22px !important;
    }

    /* Glassmorphic Output Cards */
    .glass-card {
        background: rgba(10, 16, 32, 0.8) !important;
        backdrop-filter: blur(26px) !important;
        -webkit-backdrop-filter: blur(26px) !important;
        border: 1px solid rgba(0, 242, 254, 0.22) !important;
        border-radius: 16px !important;
        padding: 22px 26px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.75), 0 0 22px -4px rgba(0, 242, 254, 0.15) !important;
    }

    /* Section Headings */
    h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.32rem !important;
        color: #f8fafc !important;
        margin: 26px 0 14px 0 !important;
        letter-spacing: -0.01em !important;
    }

    /* Personal Match Score Banner */
    .match-banner {
        background: linear-gradient(135deg, rgba(131, 56, 236, 0.22) 0%, rgba(0, 242, 254, 0.18) 100%);
        border: 1px solid rgba(0, 242, 254, 0.45);
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px -5px rgba(0, 242, 254, 0.22), 0 0 24px -2px rgba(131, 56, 236, 0.28);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 22px;
        flex-wrap: wrap;
    }

    .match-left {
        display: flex;
        align-items: center;
        gap: 20px;
        flex: 1;
        min-width: 280px;
    }

    .match-dial-box {
        width: 84px;
        height: 84px;
        border-radius: 50%;
        background: rgba(6, 12, 26, 0.9);
        border: 3.5px solid #00f2fe;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 24px rgba(0, 242, 254, 0.45);
        flex-shrink: 0;
        position: relative;
    }

    .match-pct-text {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 1.65rem;
        line-height: 1;
    }

    .match-pct-symbol {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 2px;
    }

    .match-details {
        flex: 1;
    }

    .match-category-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #00f2fe;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }

    .match-headline {
        font-size: clamp(1.15rem, 2vw, 1.42rem);
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
        font-family: 'Space Grotesk', sans-serif;
        line-height: 1.35;
    }

    .match-subtext {
        font-size: 0.94rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    .match-pills-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 12px;
    }

    .match-pill-fit {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.45);
        color: #6ee7b7;
        font-size: 0.84rem;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 500;
        line-height: 1.4;
    }

    .match-pill-tradeoff {
        background: rgba(245, 158, 11, 0.16);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #fde68a;
        font-size: 0.84rem;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 500;
        line-height: 1.4;
    }

    /* Risk Level Banners */
    .risk-banner {
        border-radius: 16px;
        padding: 20px 24px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        margin-bottom: 22px;
        font-family: 'Space Grotesk', sans-serif;
    }

    .risk-badge-group {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-shrink: 0;
        min-width: 220px;
    }

    .risk-micro-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        opacity: 0.85;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 3px;
        white-space: nowrap;
    }

    .risk-level-title {
        font-size: clamp(1.2rem, 2.2vw, 1.55rem);
        font-weight: 800;
        white-space: nowrap;
        letter-spacing: 0.02em;
    }

    .risk-lifespan-card {
        flex: 1 1 320px;
        background: rgba(0, 0, 0, 0.32);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 20px;
        text-align: left;
    }

    .risk-lifespan-value {
        font-size: 1.05rem;
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

    /* Missing Specs Badges */
    .missing-tag {
        display: inline-block;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #fca5a5;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
        margin: 4px 6px 6px 0;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* Jargon Busters */
    .analogy-card {
        background: rgba(15, 23, 42, 0.65);
        border-left: 4px solid #00f2fe;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    }

    .analogy-label {
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        color: #00f2fe;
        letter-spacing: 0.08em;
        margin-bottom: 3px;
        font-weight: 600;
    }

    .analogy-text {
        font-size: 0.98rem;
        color: #f1f5f9;
        font-style: italic;
        line-height: 1.5;
    }

    /* Persona Metric Cards */
    .persona-card {
        background: rgba(12, 20, 38, 0.82);
        border: 1px solid rgba(0, 242, 254, 0.22);
        border-radius: 14px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
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
        padding: 5px 9px;
        margin-bottom: 5px;
    }

    .pill-bottleneck {
        background: rgba(239, 68, 68, 0.16);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #fca5a5;
        font-size: 0.82rem;
        border-radius: 6px;
        padding: 5px 9px;
        margin-bottom: 5px;
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
        transition: all 0.22s ease-in-out !important;
        cursor: pointer !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 14px 35px -2px rgba(0, 242, 254, 0.8) !important;
    }

    .stButton>button:active {
        transform: translateY(1px) scale(0.99) !important;
    }

    /* Preset Buttons in Input Section */
    div[data-testid="column"] .stButton>button {
        font-size: 0.88rem !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
    }

    /* Form Inputs & Selects */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background: rgba(8, 14, 28, 0.88) !important;
        border: 1px solid rgba(0, 242, 254, 0.28) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 18px rgba(0, 242, 254, 0.35) !important;
    }

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(8, 14, 28, 0.75);
        padding: 6px 10px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        padding: 9px 18px;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 242, 254, 0.16) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.45) !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2) !important;
    }

    /* Responsive Dynamic Media Queries */
    @media (max-width: 992px) {
        div[data-testid="column"] {
            min-width: calc(50% - 0.75rem) !important;
            flex: 1 1 calc(50% - 0.75rem) !important;
            margin-bottom: 12px !important;
        }
        .risk-banner, .match-banner {
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
            padding-top: 76px !important;
        }
        .brand-title {
            font-size: 1.2rem !important;
        }
        .brand-badge, .nav-status-badge {
            display: none !important;
        }
    }

    footer {visibility: hidden;}
    </style>
    """


def get_fixed_navbar_html() -> str:
    """
    Returns the fixed top navbar HTML pinned permanently to the top of the viewport.
    """
    return """
    <div class="fixed-navbar">
        <div class="brand-section">
            <div class="brand-icon-box">⚡</div>
            <div class="brand-title">SpecSense AI</div>
            <span class="brand-badge">HARDWARE INTELLIGENCE</span>
        </div>
        <div class="nav-status-badge">
            <span class="status-dot"></span>
            <span>NEURAL ENGINE ACTIVE</span>
        </div>
    </div>
    """
