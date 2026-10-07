import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface Chatbot3DCanvasProps {
  progress?: number;
  className?: string;
}

/**
 * Proper Medium 3D Medical AI Robot Avatar.
 * - Perfectly scaled, prominent and crisp (not too small, not too large).
 * - Glossy white ceramic head & floating torso with realistic clearcoat.
 * - Glossy dark visor with expressive, glowing cyan digital eyes that blink & follow cursor.
 * - Independent floating hands with natural hover inertia.
 * - Metallic stethoscope headset with glowing cyan accent rings.
 * - Soft glowing backdrop halo behind the bot for beautiful silhouette definition.
 * - Dynamic ground shadow that scales realistically with hover altitude.
 * - Studio 3-point lighting for crisp, clean highlights.
 */
export const Chatbot3DCanvas: React.FC<Chatbot3DCanvasProps> = ({
  progress = 0,
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const width = container.clientWidth || 360;
    const height = container.clientHeight || 360;

    // 1. Scene, Camera & WebGL Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
    // Position camera closer (4.7) so robot is properly sized and prominent
    camera.position.set(0, 0, 4.7);

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.18;
    container.appendChild(renderer.domElement);

    // 2. Studio Lighting (Clean, Crisp, Professional)
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.6);
    scene.add(ambientLight);

    // Key Light: Soft White / Ice Blue from top-front
    const keyLight = new THREE.DirectionalLight(0xf0fdfa, 2.9);
    keyLight.position.set(3.5, 4.5, 4.5);
    scene.add(keyLight);

    // Fill Light: Soft Sky Blue from bottom-left
    const fillLight = new THREE.DirectionalLight(0x93c5fd, 1.5);
    fillLight.position.set(-3.5, -2, 3);
    scene.add(fillLight);

    // Rim Light: Bright Cyan highlight from top-back
    const rimLight = new THREE.DirectionalLight(0x06b6d4, 3.4);
    rimLight.position.set(0, 4, -4);
    scene.add(rimLight);

    // Subtle Eye & Chest Glow Light
    const eyePointLight = new THREE.PointLight(0x22d3ee, 1.6, 3.5);
    eyePointLight.position.set(0, 0.4, 1.2);
    scene.add(eyePointLight);

    // 3. Materials
    // Glossy White Ceramic Body
    const ceramicMat = new THREE.MeshPhysicalMaterial({
      color: 0xffffff,
      roughness: 0.12,
      metalness: 0.05,
      clearcoat: 0.95,
      clearcoatRoughness: 0.08,
    });

    // Obsidian Dark Glass Face Visor
    const visorMat = new THREE.MeshPhysicalMaterial({
      color: 0x070e1b,
      roughness: 0.08,
      metalness: 0.85,
      clearcoat: 1.0,
      clearcoatRoughness: 0.05,
    });

    // Sleek Chrome / Silver Metallic Accents
    const chromeMat = new THREE.MeshStandardMaterial({
      color: 0xdbeafe,
      metalness: 0.85,
      roughness: 0.18,
    });

    // Glowing Neon Cyan (Visor eyes, LED rings)
    const neonCyanMat = new THREE.MeshBasicMaterial({
      color: 0x00f5ff,
    });

    // Pure White Core Glow
    const pureWhiteMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
    });

    // 4. Soft Silhouette Halo Disc (Behind the robot)
    const haloDiscGeo = new THREE.CircleGeometry(1.65, 48);
    const haloDiscMat = new THREE.MeshBasicMaterial({
      color: 0x06b6d4,
      transparent: true,
      opacity: 0.09,
    });
    const haloDisc = new THREE.Mesh(haloDiscGeo, haloDiscMat);
    haloDisc.position.set(0, 0.1, -0.6);
    scene.add(haloDisc);

    // 5. Robot Master Group
    const robotRoot = new THREE.Group();
    robotRoot.position.set(0, 0.1, 0);
    scene.add(robotRoot);

    // ================= A. ROBOT HEAD =================
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.42, 0);
    robotRoot.add(headGroup);

    // Ceramic Head Sphere (Smooth & cute capsule proportion)
    const headGeo = new THREE.SphereGeometry(0.72, 48, 48);
    headGeo.scale(1.02, 0.94, 1.0);
    const headMesh = new THREE.Mesh(headGeo, ceramicMat);
    headGroup.add(headMesh);

    // Dark Curved Glass Visor (Embedded face screen)
    const visorGeo = new THREE.SphereGeometry(0.68, 36, 36, 0, Math.PI * 2, 0, Math.PI * 0.42);
    const visorMesh = new THREE.Mesh(visorGeo, visorMat);
    visorMesh.rotation.x = Math.PI * 0.52;
    visorMesh.position.set(0, 0.04, 0.12);
    headGroup.add(visorMesh);

    // Expressive Digital Visor Eyes
    const eyesGroup = new THREE.Group();
    eyesGroup.position.set(0, 0.06, 0.72);
    headGroup.add(eyesGroup);

    // Left Eye (Curved glowing pill shape)
    const eyeGeo = new THREE.CapsuleGeometry(0.065, 0.12, 16, 16);
    const leftEye = new THREE.Mesh(eyeGeo, neonCyanMat);
    leftEye.position.set(-0.24, 0, 0);
    eyesGroup.add(leftEye);

    // Left Eye Pupil Glint
    const glintGeo = new THREE.SphereGeometry(0.032, 12, 12);
    const leftGlint = new THREE.Mesh(glintGeo, pureWhiteMat);
    leftGlint.position.set(-0.24, 0.035, 0.035);
    eyesGroup.add(leftGlint);

    // Right Eye
    const rightEye = new THREE.Mesh(eyeGeo, neonCyanMat);
    rightEye.position.set(0.24, 0, 0);
    eyesGroup.add(rightEye);

    const rightGlint = new THREE.Mesh(glintGeo, pureWhiteMat);
    rightGlint.position.set(0.24, 0.035, 0.035);
    eyesGroup.add(rightGlint);

    // Stethoscope Headset & Ear Cups
    const leftEar = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.1, 24), chromeMat);
    leftEar.rotation.z = Math.PI / 2;
    leftEar.position.set(-0.74, 0, 0);
    headGroup.add(leftEar);

    const rightEar = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.18, 0.1, 24), chromeMat);
    rightEar.rotation.z = Math.PI / 2;
    rightEar.position.set(0.74, 0, 0);
    headGroup.add(rightEar);

    // Glowing cyan accent rings on ear cups
    const earLightGeo = new THREE.TorusGeometry(0.14, 0.018, 12, 24);
    const leftEarRing = new THREE.Mesh(earLightGeo, neonCyanMat);
    leftEarRing.position.set(-0.8, 0, 0);
    leftEarRing.rotation.y = Math.PI / 2;
    headGroup.add(leftEarRing);

    const rightEarRing = new THREE.Mesh(earLightGeo, neonCyanMat);
    rightEarRing.position.set(0.8, 0, 0);
    rightEarRing.rotation.y = Math.PI / 2;
    headGroup.add(rightEarRing);

    // Headband connecting the ear pieces
    const stethCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.74, 0, 0),
      new THREE.Vector3(-0.68, 0.55, 0),
      new THREE.Vector3(0, 0.76, 0),
      new THREE.Vector3(0.68, 0.55, 0),
      new THREE.Vector3(0.74, 0, 0),
    ]);
    const stethBand = new THREE.Mesh(
      new THREE.TubeGeometry(stethCurve, 28, 0.028, 10, false),
      chromeMat
    );
    headGroup.add(stethBand);

    // Forehead Medical Cross (Subtle, clean badge)
    const crossGroup = new THREE.Group();
    crossGroup.position.set(0, 0.5, 0.55);
    crossGroup.rotation.x = -0.4;
    headGroup.add(crossGroup);

    const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.16, 0.02), neonCyanMat);
    const crossH = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.045, 0.02), neonCyanMat);
    crossGroup.add(crossV);
    crossGroup.add(crossH);

    // ================= B. FLOATING TORSO (LEVITATING BODY) =================
    const torsoGroup = new THREE.Group();
    torsoGroup.position.set(0, -0.46, 0);
    robotRoot.add(torsoGroup);

    // Compact egg-shaped body
    const torsoGeo = new THREE.SphereGeometry(0.48, 36, 36);
    torsoGeo.scale(0.88, 1.15, 0.88);
    const torsoMesh = new THREE.Mesh(torsoGeo, ceramicMat);
    torsoGroup.add(torsoMesh);

    // Chest Stethoscope Tube & Medallion
    const neckDropCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-0.55, 0.42, 0.1),
      new THREE.Vector3(-0.35, 0.05, 0.38),
      new THREE.Vector3(0, -0.15, 0.46),
      new THREE.Vector3(0.35, 0.05, 0.38),
      new THREE.Vector3(0.55, 0.42, 0.1),
    ]);
    const neckTube = new THREE.Mesh(
      new THREE.TubeGeometry(neckDropCurve, 24, 0.022, 8, false),
      chromeMat
    );
    torsoGroup.add(neckTube);

    // Stethoscope Chest Sensor Bell (Disc)
    const bellMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.04, 24), chromeMat);
    bellMesh.position.set(0, -0.15, 0.48);
    bellMesh.rotation.x = Math.PI / 2.4;
    torsoGroup.add(bellMesh);

    // Glowing Cyan Core Sensor inside the bell
    const bellSensor = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.045, 24), neonCyanMat);
    bellSensor.position.set(0, -0.15, 0.485);
    bellSensor.rotation.x = Math.PI / 2.4;
    torsoGroup.add(bellSensor);

    // ================= C. FLOATING HANDS =================
    const handsGroup = new THREE.Group();
    robotRoot.add(handsGroup);

    const handGeo = new THREE.SphereGeometry(0.14, 20, 20);
    handGeo.scale(0.8, 1.3, 0.8);

    // Left Hand
    const leftHand = new THREE.Mesh(handGeo, ceramicMat);
    leftHand.position.set(-0.62, -0.42, 0.1);
    leftHand.rotation.z = 0.25;
    handsGroup.add(leftHand);

    // Right Hand
    const rightHand = new THREE.Mesh(handGeo, ceramicMat);
    rightHand.position.set(0.62, -0.42, 0.1);
    rightHand.rotation.z = -0.25;
    handsGroup.add(rightHand);

    // ================= D. CLEAN GROUND PROJECTOR & DYNAMIC SHADOW =================
    // 1. Soft Dynamic Ground Shadow
    const shadowGeo = new THREE.CircleGeometry(0.65, 32);
    const shadowMat = new THREE.MeshBasicMaterial({
      color: 0x0f172a,
      transparent: true,
      opacity: 0.28,
    });
    const groundShadow = new THREE.Mesh(shadowGeo, shadowMat);
    groundShadow.position.set(0, -1.45, 0);
    groundShadow.rotation.x = -Math.PI / 2;
    scene.add(groundShadow);

    // 2. Clean Ground Glowing Pedestal Ring
    const groundRingGeo = new THREE.RingGeometry(0.92, 0.95, 48);
    const groundRingMat = new THREE.MeshBasicMaterial({
      color: 0x00f5ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.35,
    });
    const groundRing = new THREE.Mesh(groundRingGeo, groundRingMat);
    groundRing.position.set(0, -1.44, 0);
    groundRing.rotation.x = -Math.PI / 2;
    scene.add(groundRing);

    // 6. Mouse Parallax Tracking
    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const clientX = e.clientX - rect.left;
      const clientY = e.clientY - rect.top;
      mouseRef.current.targetX = (clientX / rect.width) * 2 - 1;
      mouseRef.current.targetY = -(clientY / rect.height) * 2 + 1;
    };

    const handleMouseLeave = () => {
      mouseRef.current.targetX = 0;
      mouseRef.current.targetY = 0;
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    // 7. Smooth Animation Loop
    let animationFrameId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Smooth mouse damping
      mouseRef.current.x += (mouseRef.current.targetX - mouseRef.current.x) * 0.06;
      mouseRef.current.y += (mouseRef.current.targetY - mouseRef.current.y) * 0.06;

      // 1. Organic Levitation Physics (Smooth sinusoidal hover)
      const hoverY = Math.sin(elapsedTime * 2.4) * 0.12;
      robotRoot.position.y = 0.1 + hoverY;

      // 2. Realistic Dynamic Shadow Scale & Opacity based on height
      const shadowScale = 1 - hoverY * 1.2;
      groundShadow.scale.set(shadowScale, shadowScale, 1);
      shadowMat.opacity = 0.28 - hoverY * 0.6;

      // 3. Head & Torso Subtle Parallax Orientation towards mouse
      headGroup.rotation.y = mouseRef.current.x * 0.38;
      headGroup.rotation.x = -mouseRef.current.y * 0.28;

      torsoGroup.rotation.y = mouseRef.current.x * 0.18;
      torsoGroup.rotation.x = -mouseRef.current.y * 0.12;

      // 4. Floating Hands Inertia (delayed float)
      leftHand.position.y = -0.42 + Math.sin(elapsedTime * 2.4 - 0.4) * 0.06;
      rightHand.position.y = -0.42 + Math.sin(elapsedTime * 2.4 - 0.6) * 0.06;
      leftHand.rotation.x = -mouseRef.current.y * 0.15;
      rightHand.rotation.x = -mouseRef.current.y * 0.15;

      // 5. Expressive Eye Blinking & Looking
      const blinkCycle = elapsedTime % 3.5;
      if (blinkCycle > 3.32) {
        eyesGroup.scale.y = 0.12; // Natural blink
      } else {
        eyesGroup.scale.y = 1;
      }
      eyesGroup.position.x = mouseRef.current.x * 0.04;
      eyesGroup.position.y = 0.06 + mouseRef.current.y * 0.03;

      // 6. Ground Ring subtle pulse
      groundRing.rotation.z = -elapsedTime * 0.25;

      // 7. Halo Disc subtle pulse
      const haloPulse = 1 + Math.sin(elapsedTime * 2.0) * 0.04;
      haloDisc.scale.set(haloPulse, haloPulse, 1);

      // 8. Bell Sensor soft glow pulse
      bellSensor.scale.set(
        1 + Math.sin(elapsedTime * 3.0) * 0.06,
        1,
        1 + Math.sin(elapsedTime * 3.0) * 0.06
      );

      renderer.render(scene, camera);
    };

    animate();

    // Resize Observer
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width: newWidth, height: newHeight } = entry.contentRect;
        if (newWidth > 0 && newHeight > 0) {
          camera.aspect = newWidth / newHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(newWidth, newHeight);
        }
      }
    });
    resizeObserver.observe(container);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      resizeObserver.disconnect();
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }

      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry.dispose();
          if (Array.isArray(obj.material)) {
            obj.material.forEach((m) => m.dispose());
          } else {
            obj.material.dispose();
          }
        }
      });
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full flex items-center justify-center pointer-events-auto cursor-grab active:cursor-grabbing select-none ${className}`}
      title="Interactive 3D Clinical AI Avatar"
    />
  );
};
