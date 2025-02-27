import React, { useEffect, useRef } from 'react';
import './css/InteractiveBackground.css';

const InteractiveBackground = () => {
    const canvasRef = useRef(null);
    const mousePosition = useRef({ x: 0, y: 0 });
    const particles = useRef([]);
    const animationFrameId = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let width = window.innerWidth;
        let height = window.innerHeight;

        const resizeCanvas = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
            initParticles();
        };

        const initParticles = () => {
            particles.current = Array.from({ length: 50 }, () => ({
                x: Math.random() * width,
                y: Math.random() * height,
                size: Math.random() * 2 + 1,
                speedX: Math.random() * 2 - 1,
                speedY: Math.random() * 2 - 1,
            }));
        };

        const drawParticle = (particle) => {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0, 113, 227, 0.1)';
            ctx.fill();
        };

        const connectParticles = () => {
            for (let i = 0; i < particles.current.length; i++) {
                for (let j = i + 1; j < particles.current.length; j++) {
                    const dx = particles.current[i].x - particles.current[j].x;
                    const dy = particles.current[i].y - particles.current[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 150) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 113, 227, ${0.1 * (1 - distance / 150)})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles.current[i].x, particles.current[i].y);
                        ctx.lineTo(particles.current[j].x, particles.current[j].y);
                        ctx.stroke();
                    }
                }
            }
        };

        const animate = () => {
            ctx.clearRect(0, 0, width, height);

            particles.current.forEach(particle => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;

                const dx = mousePosition.current.x - particle.x;
                const dy = mousePosition.current.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    const angle = Math.atan2(dy, dx);
                    particle.x -= Math.cos(angle) * 0.5;
                    particle.y -= Math.sin(angle) * 0.5;
                }

                if (particle.x < 0 || particle.x > width) particle.speedX *= -1;
                if (particle.y < 0 || particle.y > height) particle.speedY *= -1;

                drawParticle(particle);
            });

            connectParticles();
            animationFrameId.current = requestAnimationFrame(animate);
        };

        const handleMouseMove = (e) => {
            mousePosition.current = {
                x: e.clientX,
                y: e.clientY,
            };
        };

        window.addEventListener('resize', resizeCanvas);
        window.addEventListener('mousemove', handleMouseMove);
        resizeCanvas();
        animate();

        return () => {
            window.removeEventListener('resize', resizeCanvas);
            window.removeEventListener('mousemove', handleMouseMove);
            if (animationFrameId.current) {
                cancelAnimationFrame(animationFrameId.current);
            }
        };
    }, []);

    return <canvas ref={canvasRef} className="interactive-background" />;
};

export default InteractiveBackground;