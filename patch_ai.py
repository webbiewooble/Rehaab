import re

with open('public/prof-body-back-base64.txt', 'r') as f:
    back_b64 = f.read().strip()

with open('ai-assessment.html', 'r') as f:
    content = f.read()

# Extract the front base64 string
front_match = re.search(r'src="data:image/jpeg;base64,([^"]+)"', content)
if front_match:
    front_b64 = front_match.group(1)
else:
    print("Could not find front image!")
    exit(1)

html_replacement = f"""
            <!-- View Toggle -->
            <div class="flex justify-center mb-6">
                <div class="bg-slate-100 p-1 rounded-full flex text-sm font-bold text-slate-500 shadow-inner">
                    <button id="view-front-btn" onclick="switchView('front')" class="px-6 py-2 rounded-full bg-white text-brand-700 shadow-sm transition-all">Front</button>
                    <button id="view-back-btn" onclick="switchView('back')" class="px-6 py-2 rounded-full hover:text-slate-700 transition-all">Back</button>
                </div>
            </div>

            <div class="flex-1 relative bg-slate-50 rounded-[2rem] border border-slate-100 p-4 flex flex-col items-center justify-center overflow-hidden">
                <!-- Grid background -->
                <div class="absolute inset-0 opacity-[0.03]" style="background-image: linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px); background-size: 20px 20px;"></div>
                
                <!-- Interactive Body Map Container -->
                <div id="body-map-container" class="relative w-full max-w-[280px] aspect-[3/4] cursor-pointer" onclick="handleBodyClick(event)">
                    
                    <!-- Front Image -->
                    <img id="body-img-front" src="data:image/jpeg;base64,{front_b64}" alt="Front Body Map" class="absolute inset-0 w-full h-full object-cover rounded-xl shadow-inner mix-blend-multiply opacity-90 transition-opacity duration-300">
                    
                    <!-- Back Image -->
                    <img id="body-img-back" src="data:image/jpeg;base64,{back_b64}" alt="Back Body Map" class="absolute inset-0 w-full h-full object-cover rounded-xl shadow-inner mix-blend-multiply opacity-0 pointer-events-none transition-opacity duration-300">

                    <!-- Dynamic Pin -->
                    <div id="dynamic-pin" class="absolute w-8 h-8 -ml-4 -mt-4 bg-brand-500/20 border-2 border-brand-500 rounded-full flex items-center justify-center hotspot-pulse opacity-0 pointer-events-none transition-all duration-200">
                        <div class="w-2 h-2 bg-brand-600 rounded-full"></div>
                    </div>
                </div>
                
                <p class="text-xs text-slate-400 mt-4 text-center z-10"><i data-lucide="info" class="w-3 h-3 inline"></i> Tap anywhere on the body to select an area.</p>
            </div>
"""

# Replace the old container (lines 186-209 in the view, roughly)
# The old container starts with <div class="flex-1 relative bg-slate-50 ... overflow-hidden">
# and ends right before <!-- Selection popover -->

start_marker = r'<div class="flex-1 relative bg-slate-50 rounded-\[2rem\] border border-slate-100 p-8 flex items-center justify-center overflow-hidden">'
end_marker = r'<!-- Selection popover -->'

pattern = start_marker + r'.*?(?=' + end_marker + r')'
content = re.sub(pattern, html_replacement, content, flags=re.DOTALL)

with open('ai-assessment.html', 'w') as f:
    f.write(content)

print("Updated HTML")
