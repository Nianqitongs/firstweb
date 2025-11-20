// 「阿彤的时光画廊」交互逻辑

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化画廊大厅
    initGalleryHall();

    // 初始化背景音乐控制
    initBGM();

    // 初始化时光轴（如果在时光轴页面）
    if (window.location.pathname.includes('timeline.html')) {
        initTimeline();
    }

    // 初始化全部展品（如果在展览页）
    if (window.location.pathname.includes('gallery.html')) {
        initGallery();
    }
});

// 1. 画廊大厅初始化
function initGalleryHall() {
    const introVideo = document.getElementById('introVideo');
    const coverImage = document.getElementById('coverImage');
    const enterButton = document.getElementById('enterButton');

    // 模拟3秒后短片淡出，显示封面
    setTimeout(() => {
        if (introVideo) {
            introVideo.style.opacity = '0';
            setTimeout(() => {
                introVideo.style.display = 'none';
            }, 1000);
        }

        // 显示封面并添加动画
        if (coverImage) {
            coverImage.classList.add('fade-in');
        }
    }, 1000); // 实际项目可改为3000ms

    // 点击"开始参观"按钮跳转到时光轴并播放音乐
    if (enterButton) {
        enterButton.addEventListener('click', () => {
            // 添加按钮点击动画
            enterButton.style.transform = 'scale(0.95)';

            // 播放背景音乐
            const bgmAudio = document.getElementById('bgmAudio');
            if (bgmAudio) {
                bgmAudio.volume = 0.3;
                bgmAudio.play().catch(err => {
                    console.log('播放失败:', err);
                });
                // 保存播放状态
                localStorage.setItem('bgmIsPlaying', 'true');
            }

            setTimeout(() => {
                window.location.href = 'timeline.html';
            }, 200);
        });
    }
}

// 2. 背景音乐控制 - 使用localStorage保存播放状态
function initBGM() {
    const bgmToggle = document.getElementById('bgmToggle');
    const bgmAudio = document.getElementById('bgmAudio');

    if (bgmToggle && bgmAudio) {
        let isPlaying = false;

        // 加载保存的播放状态
        const savedTime = localStorage.getItem('bgmTime');
        const savedIsPlaying = localStorage.getItem('bgmIsPlaying');

        if (savedTime) {
            bgmAudio.currentTime = parseFloat(savedTime);
        }

        if (savedIsPlaying === 'true') {
            bgmAudio.volume = 0.3;
            bgmAudio.play().catch(err => {
                console.log('播放失败:', err);
            });
            isPlaying = true;
            bgmToggle.textContent = '🔇 关闭音乐';
        }

        // 点击切换音乐播放状态
        bgmToggle.addEventListener('click', () => {
            if (isPlaying) {
                bgmAudio.pause();
                bgmToggle.textContent = '🎵 背景音乐';
            } else {
                bgmAudio.volume = 0.3;
                bgmAudio.play().catch(err => {
                    console.log('播放失败:', err);
                });
                bgmToggle.textContent = '🔇 关闭音乐';
            }
            isPlaying = !isPlaying;
            // 保存播放状态
            localStorage.setItem('bgmIsPlaying', isPlaying);
        });

        // 保存播放状态和时间当页面卸载时
        window.addEventListener('beforeunload', () => {
            localStorage.setItem('bgmTime', bgmAudio.currentTime);
            localStorage.setItem('bgmIsPlaying', isPlaying);
        });
    }
}
// 3. 时光轴初始化
function initTimeline() {
    const memoryCapsules = document.querySelectorAll('.memory-capsule');
    const diptychZone = document.getElementById('diptychZone');
    const diptychItems = document.querySelectorAll('.diptych-item');
    const shareButton = document.getElementById('shareButton');

    // 实现时光轴图片懒加载
    const lazyImages = document.querySelectorAll('.memory-capsule img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
        });
    });

    lazyImages.forEach(image => {
        imageObserver.observe(image);
    });

    // 记忆胶囊交互
    memoryCapsules.forEach(capsule => {
        // 鼠标悬停放大效果（已通过CSS实现，这里可添加额外交互）
        // 点击事件已在timeline.html中实现模态画廊功能，故注释掉此处默认点击事件
        // capsule.addEventListener('click', () => {
        //     const imageUrl = capsule.querySelector('.capsule-image img').src;
        //     const date = capsule.querySelector('.capsule-date').textContent;
        //     const location = capsule.querySelector('.capsule-location').textContent;

        //     console.log('点击了记忆胶囊:', date, location);
        //     // 这里可以实现点击后查看大图功能
        // });

        // 拖拽功能 - 长按开始拖拽
        let longPressTimer;
        let isDragging = false;
        let draggedCapsule = null;

        capsule.addEventListener('mousedown', (e) => {
            longPressTimer = setTimeout(() => {
                isDragging = true;
                draggedCapsule = capsule;
                capsule.style.cursor = 'grabbing';
                // 提升z-index
                capsule.style.zIndex = '1000';
            }, 500); // 500ms长按触发拖拽
        });

        // 释放鼠标或离开元素时结束拖拽
        capsule.addEventListener('mouseup', () => {
            clearTimeout(longPressTimer);
            if (isDragging) {
                isDragging = false;
                capsule.style.cursor = 'pointer';
                capsule.style.zIndex = '1';
            }
        });

        capsule.addEventListener('mouseleave', () => {
            clearTimeout(longPressTimer);
            if (isDragging) {
                isDragging = false;
                capsule.style.cursor = 'pointer';
                capsule.style.zIndex = '1';
            }
        });

        // 拖拽移动
        document.addEventListener('mousemove', (e) => {
            if (isDragging && draggedCapsule) {
                const rect = draggedCapsule.getBoundingClientRect();
                draggedCapsule.style.position = 'fixed';
                draggedCapsule.style.left = `${e.clientX - rect.width / 2}px`;
                draggedCapsule.style.top = `${e.clientY - rect.height / 2}px`;
            }
        });

        // 拖拽到对比区
        if (diptychZone) {
            diptychZone.addEventListener('mouseup', () => {
                if (isDragging && draggedCapsule) {
                    const diptychSlots = diptychZone.querySelectorAll('.diptych-slot');
                    // 查找空的对比槽位
                    for (const slot of diptychSlots) {
                        if (!slot.hasAttribute('data-filled')) {
                            // 将拖拽的胶囊信息填充到对比槽位
                            const imageUrl = draggedCapsule.querySelector('.capsule-image img').src;
                            const date = draggedCapsule.querySelector('.capsule-date').textContent;
                            const location = draggedCapsule.querySelector('.capsule-location').textContent;

                            // 加载图片到对比区
                            const imgElement = slot.querySelector('.diptych-image');
                            const dateElement = slot.querySelector('.diptych-date');
                            const emotionElement = slot.querySelector('.diptych-emotion');

                            if (imgElement) {
                                imgElement.src = imageUrl;
                            }
                            if (dateElement) {
                                dateElement.textContent = date;
                            }
                            if (emotionElement) {
                                // 这里可以添加AI生成的情感关键词
                                emotionElement.textContent = getRandomEmotion();
                            }

                            // 标记为已填充
                            slot.setAttribute('data-filled', 'true');
                            slot.setAttribute('data-image-url', imageUrl);
                            slot.setAttribute('data-date', date);

                            // 显示对比区
                            diptychZone.classList.remove('hidden');

                            break;
                        }
                    }

                    // 重置拖拽状态
                    isDragging = false;
                    draggedCapsule.style.position = '';
                    draggedCapsule.style.left = '';
                    draggedCapsule.style.top = '';
                    draggedCapsule.style.cursor = 'pointer';
                    draggedCapsule.style.zIndex = '1';
                    draggedCapsule = null;
                }
            });
        }
    });

    // 分享按钮功能
    if (shareButton) {
        shareButton.addEventListener('click', () => {
            // 生成带水印的对比图（模拟实现）
            alert('分享功能开发中...\n将生成带水印的对比图PNG文件');
            // 实际项目中可使用canvas合成两张图片并添加水印
        });
    }

    // 键盘左右键控制时光轴滚动
    document.addEventListener('keydown', (e) => {
        const timeline = document.querySelector('.timeline-horizontal');
        if (!timeline) return;

        const scrollAmount = 200; // 滚动距离

        if (e.key === 'ArrowLeft') {
            timeline.scrollLeft -= scrollAmount;
        } else if (e.key === 'ArrowRight') {
            timeline.scrollLeft += scrollAmount;
        }
    });
}

// 4. 全部展品初始化
function initGallery() {
    const exhibitCards = document.querySelectorAll('.exhibit-card');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // 实现图片懒加载
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
        });
    });

    lazyImages.forEach(image => {
        imageObserver.observe(image);
    });

    // 加载完成动画
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
        setTimeout(() => {
            exhibitCards.forEach((card, index) => {
                card.style.animation = `fadeIn 0.6s ease forwards ${index * 0.1}s`;
            });
            loadingSpinner.style.display = 'none';
        }, 800);
    }

    // 展品卡片交互
    exhibitCards.forEach(card => {
        card.addEventListener('click', () => {
            const imgUrl = card.querySelector('img').src;
            const date = card.getAttribute('data-date');
            const location = card.getAttribute('data-location');

            // 这里可以实现大图预览功能
            console.log('查看展品:', date, location);
        });
    });
}

// 辅助函数：获取随机情感关键词
function getRandomEmotion() {
    const emotions = ['夏日', '成长', '重逢', '温暖', '快乐', '陪伴', '回忆', '美好', '幸福', '感动'];
    return emotions[Math.floor(Math.random() * emotions.length)];
}

// 辅助函数：计算时间差
function calculateTimeDiff(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const diffTime = Math.abs(d2 - d1);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    const diffMonths = Math.abs(d2.getMonth() - d1.getMonth() + (12 * (d2.getFullYear() - d1.getFullYear())));

    if (diffMonths > 12) {
        const diffYears = Math.floor(diffMonths / 12);
        return `${diffYears}年${diffMonths % 12}个月`;
    } else if (diffMonths > 0) {
        return `${diffMonths}个月${diffDays % 30}天`;
    } else {
        return `${diffDays}天`;
    }
}

// 辅助函数：生成带水印的图片（模拟）
function generateWatermarkedImage(img1, img2) {
    // 这里使用canvas实现图片合成和水印添加
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 400;
    const ctx = canvas.getContext('2d');

    // 绘制背景
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 绘制两张图片
    const imgElement1 = new Image();
    imgElement1.crossOrigin = 'anonymous';
    imgElement1.src = img1;

    const imgElement2 = new Image();
    imgElement2.crossOrigin = 'anonymous';
    imgElement2.src = img2;

    // 等图片加载完成后绘制
    Promise.all([
        new Promise(resolve => imgElement1.onload = resolve),
        new Promise(resolve => imgElement2.onload = resolve)
    ]).then(() => {
        // 绘制第一张图片
        ctx.drawImage(imgElement1, 50, 50, 550, 300);

        // 绘制第二张图片
        ctx.drawImage(imgElement2, 600, 50, 550, 300);

        // 添加水印
        ctx.fillStyle = 'rgba(212, 184, 140, 0.5)';
        ctx.font = '48px "Playfair Display", serif';
        ctx.textAlign = 'center';
        ctx.fillText('阿彤的时光画廊', canvas.width / 2, canvas.height / 2);

        // 生成PNG文件
        const dataUrl = canvas.toDataURL('image/png');

        // 下载图片
        const downloadLink = document.createElement('a');
        downloadLink.href = dataUrl;
        downloadLink.download = 'atong-comparison.png';
        downloadLink.click();
    });
}

// 响应式处理
function handleResponsive() {
    const isMobile = window.innerWidth < 768;

    // 根据屏幕尺寸调整交互
    const timeline = document.querySelector('.timeline-horizontal');
    if (timeline) {
        if (isMobile) {
            // 移动端使用垂直时间轴
            timeline.classList.remove('timeline-horizontal');
            timeline.classList.add('timeline-vertical');
        } else {
            // 桌面端使用横向时间轴
            timeline.classList.add('timeline-horizontal');
            timeline.classList.remove('timeline-vertical');
        }
    }
}

// 窗口大小变化时处理响应式
window.addEventListener('resize', handleResponsive);

// 初始化时检查响应式
handleResponsive();

// 获取随机图片路径（用于测试）
function getRandomImagePath() {
    const folders = ['精修', 'jpg'];
    const folder = folders[Math.floor(Math.random() * folders.length)];

    // 这里需要根据实际图片数量调整
    const imgNumber = Math.floor(Math.random() * 50) + 1; // 假设有50张图片
    const extensions = ['jpg', 'png'];
    const extension = extensions[Math.floor(Math.random() * extensions.length)];

    return `${folder}/${imgNumber}.${extension}`;
}

// 自动生成时光轴内容（模拟）
function generateTimelineContent() {
    const timelineContainer = document.getElementById('timelineContainer');
    if (!timelineContainer) return;

    // 模拟数据 - 实际项目应从后端获取
    const memories = [
        {
            date: '2023.05.20',
            location: '厦门',
            imageUrl: '精修/051A8523 拷贝.jpg'
        },
        {
            date: '2023.08.15',
            location: '杭州',
            imageUrl: '精修/051A8523 拷贝.jpg'
        },
        {
            date: '2023.10.01',
            location: '北京',
            imageUrl: '精修/051A8523 拷贝.jpg'
        },
        {
            date: '2024.02.14',
            location: '上海',
            imageUrl: '精修/051A8523 拷贝.jpg'
        }
    ];

    // 生成记忆胶囊
    memories.forEach(memory => {
        const capsule = document.createElement('div');
        capsule.className = 'memory-capsule fade-in';

        capsule.innerHTML = `
            <div class="capsule-image">
                <img src="${memory.imageUrl}" alt="${memory.date}">
            </div>
            <div class="capsule-info">
                <div class="capsule-date">${memory.date}</div>
                <div class="capsule-location">${memory.location}</div>
            </div>
        `;

        timelineContainer.appendChild(capsule);
    });
}

// AI情感分析模拟（实际项目可对接AI API）
function analyzeEmotion(imageUrl) {
    // 模拟AI分析结果
    const emotions = ['开心', '温柔', '成长', '幸福', '感动', '浪漫', '温暖', '美好'];
    return emotions[Math.floor(Math.random() * emotions.length)];
}