#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random

# Set base directories
base_dir = r"D:\workspace\files\照片\时光画廊"
website_dir = r"D:\workspace\files\照片"

# List all folders
folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f not in ['.', '..']]

# Sort folders by name
folders.sort()

# Generate HTML for timeline nodes
timeline_nodes = []

for i, folder in enumerate(folders):
    # Get all image files in the folder
    folder_path = os.path.join(base_dir, folder)
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if images:
        # Select one image for the node thumbnail
        thumbnail = os.path.relpath(os.path.join(folder_path, images[0]), website_dir)

        # Generate random date
        year = random.randint(2020, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = f"{year}.{month:02d}.{day:02d}"

        # Generate node title from folder name
        title = folder[3:]  # Remove the number prefix

        # Create node HTML
        node_html = f'''
        <div class="memory-capsule fade-in" data-folder="{folder}" data-title="{title}" data-thumbnail="{thumbnail}">
            <div class="capsule-image">
                <img data-src="{thumbnail}" alt="{title}" class="lazy">
            </div>
            <div class="capsule-info">
                <div class="capsule-date">{date}</div>
                <div class="capsule-location">{title}</div>
            </div>
        </div>
        '''

        timeline_nodes.append(node_html)

# Generate the timeline content
timeline_content = ''.join(timeline_nodes)

# Read the existing timeline.html file
with open(os.path.join(website_dir, 'timeline.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# Find the timeline container and replace its content
start_marker = '<!-- 横向时光轴 -->\n        <div class="timeline-horizontal" id="timelineContainer">'
end_marker = '</div>\n    </div>\n\n    <!-- 双联画对比区 -->'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("找不到 timelineContainer 开始标记")
else:
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("找不到 timelineContainer 结束标记")
    else:
        # Update the timeline content
        new_content = content[:start_idx + len(start_marker)] + '\n' + timeline_content + '\n        ' + content[end_idx:]

        # Add the popup modal HTML
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

    <style>
    /* 图片画廊弹窗样式 */
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
        animation: fadeInModal 0.5s ease;
    }

    .modal-content {
        margin: 5% auto;
        padding: 20px;
        width: 80%;
        max-width: 1200px;
        background-color: rgba(248, 245, 240, 0.98);
        border-radius: 12px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }

    .close-modal {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.3s ease;
    }

    .close-modal:hover,
    .close-modal:focus {
        color: #333;
        text-decoration: none;
        cursor: pointer;
    }

    #modalTitle {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 2px solid var(--secondary-color);
        padding-bottom: 10px;
    }

    .modal-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }

    /* 动画效果 */
    @keyframes fadeInModal {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .modal-content {
            margin: 10% auto;
            width: 95%;
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

        # Add the modal HTML before the closing body tag
        body_close_idx = new_content.rfind('</body>')
        if body_close_idx != -1:
            new_content = new_content[:body_close_idx] + modal_html + new_content[body_close_idx:]

        # Write the updated content back
        with open(os.path.join(website_dir, 'timeline.html'), 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("更新了 timeline.html 的时光轴节点和弹窗")

# Generate JavaScript to handle modal
modal_js = '''
// 初始化时光轴模态框
function initGalleryModal() {
    const modal = document.getElementById('galleryModal');
    const closeBtn = document.querySelector('.close-modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalGallery = document.getElementById('modalGallery');
    const baseDir = '时光画廊';

    // 点击记忆胶囊打开模态框
    document.querySelectorAll('.memory-capsule').forEach(capsule => {
        capsule.addEventListener('click', () => {
            const folder = capsule.dataset.folder;
            const title = capsule.dataset.title;
            const thumbnail = capsule.dataset.thumbnail;

            // 设置模态框标题
            modalTitle.textContent = title;

            // 清空画廊内容
            modalGallery.innerHTML = '';

            // 使用 fetch 获取文件夹中的所有图片（这里需要服务器支持，暂时使用静态方式）
            // For now, we'll hardcode the image list (in a real server environment, we'd use an API)

            // 实际上，由于安全限制，JavaScript无法直接读取本地文件系统的文件列表
            // 因此我们需要生成一个包含所有图片路径的JSON文件或在HTML中嵌入数据

            // 以下是一个模拟示例
            const mockImages = [
                '时光画廊/01_合照/image1.jpg',
                '时光画廊/01_合照/image2.jpg',
                '时光画廊/01_合照/image3.jpg'
            ];

            // 加载图片（实际项目中需要动态生成这个列表）
            const folderImages = mockImages.filter(img => img.startsWith(baseDir + '/' + folder));

            if (folderImages.length === 0) {
                modalGallery.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 50px 0;">该相册暂无照片</p>';
            } else {
                folderImages.forEach(img => {
                    const imgElement = document.createElement('img');
                    imgElement.src = img;
                    imgElement.alt = title;
                    modalGallery.appendChild(imgElement);
                });
            }

            // 显示模态框
            modal.style.display = 'block';
        });
    });

    // 点击关闭按钮关闭模态框
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // 点击模态框外部关闭模态框
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// 在初始化时调用
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    initGalleryModal();
});
'''

# For now, we need to handle this differently since we can't read local files from JavaScript

print("\n已完成时光轴节点生成")
print("\n接下来需要注意：")
print("1. JavaScript无法直接读取本地文件系统的文件列表")
print("2. 需要将所有图片路径嵌入到HTML或JSON中")
print("3. 已生成基本的模态框结构，需要手动更新图片路径")