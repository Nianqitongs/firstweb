#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import json

# Set base directories
base_dir = r"D:\workspace\files\照片"
timeline_dir = r"D:\workspace\files\照片\时光画廊"

# List all folders
folders = [f for f in os.listdir(timeline_dir) if os.path.isdir(os.path.join(timeline_dir, f)) and f not in ['.', '..']]
folders.sort()

# Generate timeline data
timeline_data = []
folder_images = {}

for i, folder in enumerate(folders):
    folder_path = os.path.join(timeline_dir, folder)
    images = [os.path.join(timeline_dir, folder, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if images:
        # Select specific thumbnail based on folder name
        if folder == "04_云南旅游" and len(images) >= 3:
            thumbnail = images[2]  # Use 旅游3.jpg (index 2 for 0-based)
        elif folder == "05_日常美照" and len(images) >= 3:
            thumbnail = images[2]  # Use 日常美照3.jpg (index 2 for 0-based)
        else:
            thumbnail = images[0]

        # Generate random date
        year = random.randint(2022, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = f"{year}.{month:02d}.{day:02d}"

        # Clean up paths for web
        thumbnail_web = thumbnail.replace(base_dir + '\\', '').replace('\\', '/')

        # Add to timeline data
        timeline_data.append({
            "id": i,
            "folder": folder,
            "title": folder[3:],  # Remove prefix
            "date": date,
            "thumbnail": thumbnail_web,
            "images": [img.replace(base_dir + '\\', '').replace('\\', '/') for img in images]
        })

        # Store images by folder
        folder_images[folder] = [img.replace(base_dir + '\\', '').replace('\\', '/') for img in images]

# Read existing timeline.html
timeline_html_path = os.path.join(base_dir, 'timeline.html')
with open(timeline_html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Generate timeline nodes HTML
timeline_nodes_html = ""
for item in timeline_data:
    timeline_nodes_html += f'''
    <div class="memory-capsule fade-in" data-folder="{item['folder']}" data-title="{item['title']}">
        <div class="capsule-image">
            <img data-src="{item['thumbnail']}" alt="{item['title']}" class="lazy">
        </div>
        <div class="capsule-info">
            <div class="capsule-date">{item['date']}</div>
            <div class="capsule-location">{item['title']}</div>
        </div>
    </div>
    '''

# Update the timeline container
start_marker = '<!-- 横向时光轴 -->\n        <div class="timeline-horizontal" id="timelineContainer">'
end_marker = '</div>\n    </div>\n\n    <!-- 双联画对比区 -->'

if start_marker in html_content and end_marker in html_content:
    start_idx = html_content.find(start_marker) + len(start_marker)
    end_idx = html_content.find(end_marker)
    new_html_content = html_content[:start_idx] + '\n' + timeline_nodes_html + '\n        ' + html_content[end_idx:]
    html_content = new_html_content

# Generate modal HTML
modal_html = '''
    <!-- 图片画廊弹窗 -->
    <div id="galleryModal" class="gallery-modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2 id="modalTitle"></h2>
            <div class="modal-gallery" id="modalGallery">
                <!-- 图片将通过JavaScript动态加载 -->
            </div>
        </div>
    </div>
'''

# Generate modal CSS
modal_css = '''
<style>
.gallery-modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.9);
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background-color: var(--primary-color);
    margin: 5% auto;
    padding: 30px;
    width: 85%;
    max-width: 1200px;
    border-radius: 12px;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
    animation: slideUp 0.3s ease;
}

.close-modal {
    color: var(--text-primary);
    float: right;
    font-size: 35px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.close-modal:hover {
    color: var(--accent-color);
    transform: rotate(180deg);
}

#modalTitle {
    font-family: var(--serif-font);
    font-size: 2.5rem;
    color: var(--text-primary);
    margin-bottom: 30px;
    text-align: center;
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 10px;
}

.modal-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

.modal-gallery img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}

.modal-gallery img:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@media (max-width: 768px) {
    .modal-content {
        margin: 10% auto;
        width: 95%;
        padding: 20px;
    }

    #modalTitle {
        font-size: 1.8rem;
    }

    .modal-gallery {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 15px;
    }

    .modal-gallery img {
        height: 150px;
    }
}
</style>
'''

# Generate modal JavaScript
modal_js = f'''
<script>
// 时光轴图片数据
const timelineImageData = {json.dumps(folder_images, ensure_ascii=False)};

// 初始化画廊模态框
function initGalleryModal() {{
    const modal = document.getElementById('galleryModal');
    const closeBtn = document.querySelector('.close-modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalGallery = document.getElementById('modalGallery');

    // 点击记忆胶囊打开模态框
    document.querySelectorAll('.memory-capsule').forEach(capsule => {{
        capsule.addEventListener('click', () => {{
            const folder = capsule.dataset.folder;
            const title = capsule.dataset.title;

            // 设置标题
            modalTitle.textContent = title;

            // 加载图片
            const images = timelineImageData[folder] || [];
            modalGallery.innerHTML = '';

            if (images.length > 0) {{
                images.forEach(imageUrl => {{
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.alt = title;
                    modalGallery.appendChild(img);
                }});
            }} else {{
                modalGallery.innerHTML = '<p style="text-align: center; padding: 50px 0; color: var(--text-secondary);">该相册暂无照片</p>';
            }}

            // 显示模态框
            modal.style.display = 'block';
        }});
    }});

    // 关闭模态框
    closeBtn.addEventListener('click', () => {{
        modal.style.display = 'none';
    }});

    // 点击外部关闭
    window.addEventListener('click', (e) => {{
        if (e.target === modal) {{
            modal.style.display = 'none';
        }}
    }});
}}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initGalleryModal);
</script>
'''

# Add all modal components to the HTML
all_modal_html = f'''
{modal_css}
{modal_html}
{modal_js}
'''

# Insert before the closing body tag
html_content = html_content.replace('</body>', all_modal_html + '</body>')

# Write the updated HTML
with open(timeline_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ 生成了时光轴节点")
print("✓ 生成了画廊模态框")
print("✓ 嵌入了图片数据")
print("\n完成！")

# Generate backup JSON
with open(os.path.join(base_dir, 'timeline_data.json'), 'w', encoding='utf-8') as f:
    json.dump(timeline_data, f, ensure_ascii=False, indent=2)
print("✓ 生成了 timeline_data.json 备份文件")
