import re

with open('ai-assessment.html', 'r') as f:
    content = f.read()

js_code = """
    let currentView = 'front';
    
    function switchView(view) {
        currentView = view;
        const frontImg = document.getElementById('body-img-front');
        const backImg = document.getElementById('body-img-back');
        const frontBtn = document.getElementById('view-front-btn');
        const backBtn = document.getElementById('view-back-btn');
        
        // Hide pin on switch
        document.getElementById('dynamic-pin').style.opacity = '0';
        document.getElementById('selection-popover').classList.remove('translate-y-0', 'opacity-100');
        document.getElementById('selection-popover').classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
        
        if (view === 'front') {
            frontImg.style.opacity = '0.9';
            backImg.style.opacity = '0';
            frontBtn.classList.add('bg-white', 'text-brand-700', 'shadow-sm');
            frontBtn.classList.remove('hover:text-slate-700');
            backBtn.classList.remove('bg-white', 'text-brand-700', 'shadow-sm');
            backBtn.classList.add('hover:text-slate-700');
        } else {
            frontImg.style.opacity = '0';
            backImg.style.opacity = '0.9';
            backBtn.classList.add('bg-white', 'text-brand-700', 'shadow-sm');
            backBtn.classList.remove('hover:text-slate-700');
            frontBtn.classList.remove('bg-white', 'text-brand-700', 'shadow-sm');
            frontBtn.classList.add('hover:text-slate-700');
        }
    }

    const frontPoints = [
        { name: 'Head', x: 50, y: 10 },
        { name: 'Neck', x: 50, y: 19 },
        { name: 'Right Shoulder', x: 30, y: 25 },
        { name: 'Left Shoulder', x: 70, y: 25 },
        { name: 'Chest', x: 50, y: 30 },
        { name: 'Abdomen', x: 50, y: 45 },
        { name: 'Right Bicep', x: 22, y: 40 },
        { name: 'Left Bicep', x: 78, y: 40 },
        { name: 'Right Forearm', x: 15, y: 55 },
        { name: 'Left Forearm', x: 85, y: 55 },
        { name: 'Pelvis/Groin', x: 50, y: 56 },
        { name: 'Right Hand', x: 10, y: 70 },
        { name: 'Left Hand', x: 90, y: 70 },
        { name: 'Right Thigh', x: 40, y: 68 },
        { name: 'Left Thigh', x: 60, y: 68 },
        { name: 'Right Knee', x: 40, y: 80 },
        { name: 'Left Knee', x: 60, y: 80 },
        { name: 'Right Shin', x: 40, y: 90 },
        { name: 'Left Shin', x: 60, y: 90 },
        { name: 'Right Foot', x: 38, y: 98 },
        { name: 'Left Foot', x: 62, y: 98 }
    ];

    const backPoints = [
        { name: 'Back of Head', x: 50, y: 10 },
        { name: 'Back of Neck', x: 50, y: 19 },
        { name: 'Left Rear Shoulder', x: 30, y: 25 },
        { name: 'Right Rear Shoulder', x: 70, y: 25 },
        { name: 'Upper Back', x: 50, y: 30 },
        { name: 'Lower Back', x: 50, y: 45 },
        { name: 'Left Tricep', x: 22, y: 40 },
        { name: 'Right Tricep', x: 78, y: 40 },
        { name: 'Left Forearm', x: 15, y: 55 },
        { name: 'Right Forearm', x: 85, y: 55 },
        { name: 'Glutes', x: 50, y: 56 },
        { name: 'Left Hand', x: 10, y: 70 },
        { name: 'Right Hand', x: 90, y: 70 },
        { name: 'Left Hamstring', x: 40, y: 68 },
        { name: 'Right Hamstring', x: 60, y: 68 },
        { name: 'Left Back of Knee', x: 40, y: 80 },
        { name: 'Right Back of Knee', x: 60, y: 80 },
        { name: 'Left Calf', x: 40, y: 90 },
        { name: 'Right Calf', x: 60, y: 90 },
        { name: 'Left Heel', x: 38, y: 98 },
        { name: 'Right Heel', x: 62, y: 98 }
    ];

    function handleBodyClick(event) {
        const container = document.getElementById('body-map-container');
        const rect = container.getBoundingClientRect();
        
        // Calculate percentage coordinates
        const x = ((event.clientX - rect.left) / rect.width) * 100;
        const y = ((event.clientY - rect.top) / rect.height) * 100;
        
        const points = currentView === 'front' ? frontPoints : backPoints;
        
        // Find nearest point
        let nearest = points[0];
        let minDistance = Infinity;
        
        for (const pt of points) {
            const dx = pt.x - x;
            const dy = pt.y - y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < minDistance) {
                minDistance = dist;
                nearest = pt;
            }
        }
        
        // If they click way off into empty space, maybe ignore. (e.g. max dist 20%)
        if(minDistance > 25) return;

        // Move pin
        const pin = document.getElementById('dynamic-pin');
        pin.style.left = nearest.x + '%';
        pin.style.top = nearest.y + '%';
        pin.style.opacity = '1';
        
        // Select part
        selectBodyPart(nearest.name);
    }
"""

# inject right before `function selectBodyPart(part)`
content = re.sub(r'(function selectBodyPart\([^)]+\) {)', js_code + r'\n    \1', content)

with open('ai-assessment.html', 'w') as f:
    f.write(content)

print("Updated JS")
