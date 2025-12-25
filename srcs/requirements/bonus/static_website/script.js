// ==================== PROJECT DATA ====================
const projectData = {
    libft: {
        title: "Libft - Custom C Library",
        objectives: "Create a library of custom implementations of standard C library functions. This serves as the foundation for all future 42 projects and teaches fundamental C programming concepts.",
        challenges: [
            "Understanding memory allocation with malloc and free",
            "Implementing string manipulation functions from scratch",
            "Creating and managing linked list data structures",
            "Following strict coding standards (Norminette)",
            "Writing a comprehensive Makefile"
        ],
        learned: [
            "Deep understanding of C standard library functions",
            "Memory management and pointer manipulation",
            "Code organization and library creation",
            "Writing reusable and efficient code",
            "Thorough testing and edge case handling"
        ]
    },
    gnl: {
        title: "Get_Next_Line - File Reading Function",
        objectives: "Implement a function that reads a line from a file descriptor, handling multiple file descriptors simultaneously and managing dynamic buffer allocation.",
        challenges: [
            "Managing static variables across function calls",
            "Handling buffer overflow and memory leaks",
            "Reading from multiple file descriptors",
            "Dealing with different buffer sizes",
            "Edge cases: empty files, no newline at EOF"
        ],
        learned: [
            "File I/O operations in C",
            "Static variable behavior and scope",
            "Dynamic memory management",
            "Buffer handling techniques",
            "Debugging complex memory issues"
        ]
    },
    pushswap: {
        title: "Push_swap - Sorting Algorithm",
        objectives: "Sort a stack of integers using only two stacks and a limited set of operations. The challenge is to minimize the number of operations required.",
        challenges: [
            "Developing efficient sorting algorithms",
            "Optimizing for minimal operations",
            "Handling edge cases (duplicates, sorted input)",
            "Implementing visualization tools",
            "Testing with various input sizes"
        ],
        learned: [
            "Algorithm design and optimization",
            "Big O notation and complexity analysis",
            "Stack data structure implementation",
            "Problem decomposition strategies",
            "Performance benchmarking"
        ]
    },
    minishell: {
        title: "Minishell - Unix Shell Implementation",
        objectives: "Create a functional Unix shell with features like pipes, redirections, environment variables, signal handling, and built-in commands.",
        challenges: [
            "Parsing complex command line input",
            "Managing multiple processes with fork/exec",
            "Implementing pipe and redirection logic",
            "Handling signals (Ctrl+C, Ctrl+D, Ctrl+\\)",
            "Managing environment variables"
        ],
        learned: [
            "Process creation and management",
            "Inter-process communication (pipes)",
            "Signal handling in Unix systems",
            "Lexical analysis and parsing",
            "Collaborative programming (pair project)"
        ]
    },
    philosophers: {
        title: "Philosophers - Concurrency Problem",
        objectives: "Solve the classic dining philosophers problem using threads and mutexes. Prevent deadlocks while ensuring philosophers can eat, think, and sleep.",
        challenges: [
            "Preventing deadlock conditions",
            "Avoiding race conditions with mutexes",
            "Precise timing and synchronization",
            "Detecting philosopher death accurately",
            "Managing multiple threads efficiently"
        ],
        learned: [
            "Multithreading with pthreads",
            "Mutex synchronization techniques",
            "Deadlock prevention strategies",
            "Concurrent programming patterns",
            "Thread-safe programming practices"
        ]
    },
    cub3d: {
        title: "Cub3D - 3D Game Engine",
        objectives: "Build a 3D game engine inspired by Wolfenstein 3D using raycasting. Implement texture mapping, collision detection, and real-time rendering.",
        challenges: [
            "Implementing raycasting algorithm from scratch",
            "Texture mapping on walls",
            "Optimizing rendering performance",
            "Handling player movement and collision",
            "Parsing map configuration files"
        ],
        learned: [
            "Computer graphics fundamentals",
            "Raycasting and 3D projection",
            "Graphics library usage (MLX)",
            "Game loop and event handling",
            "Mathematical concepts (vectors, angles)"
        ]
    },
    cpp: {
        title: "CPP Modules - Object-Oriented Programming",
        objectives: "Master C++ through progressive modules covering OOP principles, memory management, inheritance, polymorphism, operator overloading, templates, and STL containers.",
        challenges: [
            "Understanding the C++ Orthodox Canonical Form",
            "Implementing operator overloading correctly",
            "Managing deep vs shallow copying",
            "Working with abstract classes and interfaces",
            "Mastering template programming and STL",
            "Understanding RAII and exception safety"
        ],
        learned: [
            "Object-oriented programming principles",
            "C++ memory management (stack vs heap)",
            "Polymorphism and virtual functions",
            "Template metaprogramming basics",
            "STL containers and algorithms",
            "Best practices for modern C++ code"
        ]
    },
    netpractice: {
        title: "NetPractice - Network Configuration",
        objectives: "Understand and configure network addressing through practical exercises. Master TCP/IP, subnetting, routing tables, and network troubleshooting in simulated environments.",
        challenges: [
            "Calculating subnet masks and CIDR notation",
            "Configuring routing tables correctly",
            "Understanding broadcast and network addresses",
            "Solving complex network topology problems",
            "Debugging connectivity issues",
            "Working with different network classes"
        ],
        learned: [
            "TCP/IP protocol suite fundamentals",
            "Subnetting and IP addressing schemes",
            "Routing concepts and path selection",
            "Network layer operations (Layer 3)",
            "Binary and hexadecimal conversions",
            "Network troubleshooting methodology"
        ]
    },
    inception: {
        title: "Inception - Docker Infrastructure",
        objectives: "Set up a complete multi-container infrastructure using Docker and Docker Compose. Deploy NGINX, WordPress, MariaDB with volumes, networks, and custom configurations.",
        challenges: [
            "Writing efficient Dockerfiles from scratch",
            "Configuring secure inter-container networking",
            "Managing persistent data with volumes",
            "Setting up SSL/TLS certificates",
            "Orchestrating services with Docker Compose",
            "Following security best practices",
            "Debugging container networking issues"
        ],
        learned: [
            "Docker containerization concepts",
            "Docker Compose orchestration",
            "System administration fundamentals",
            "NGINX web server configuration",
            "Database management and security",
            "Network isolation and container security",
            "Infrastructure as Code principles"
        ]
    },
    ftirc: {
        title: "ft_irc - IRC Server Implementation",
        objectives: "Build a fully functional IRC server in C++98 that handles multiple clients simultaneously. Implement IRC protocol commands, channel management, and private messaging.",
        challenges: [
            "Implementing non-blocking I/O with select/poll/epoll",
            "Managing multiple client connections efficiently",
            "Parsing and validating IRC protocol commands",
            "Handling channel operations (join, part, kick, etc.)",
            "Implementing user authentication and modes",
            "Managing server state and client permissions",
            "Error handling and edge cases"
        ],
        learned: [
            "Network socket programming",
            "I/O multiplexing techniques",
            "IRC protocol specifications (RFC 1459)",
            "Client-server architecture patterns",
            "Concurrent connection handling",
            "State management in networked applications",
            "Protocol implementation and testing"
        ]
    },
    'transcendence_ai': {
        title: '_transcendence – AI Module',
        objectives: 'Enhanced a Pong platform with four AI features: a human-like game opponent, a RAG support system, an LLM chat interface, and a recommendation system.',
        challenges: [
            'Creating balanced game AI that feels human',
            'Building efficient RAG retrieval for game support',
            'Integrating LLM chat within real-time game architecture',
            'Training ML recommendations from user match data',
            'Optimizing AI performance with existing WebSockets'
        ],
        learned: [
            'Reinforcement learning for game opponents',
            'RAG system design and implementation',
            'LLM integration patterns for applications',
            'Feature engineering for recommendation systems',
            'Real-time AI architecture optimization'
        ]
    },
    'medicinal_plant': {
        title: 'Medicinal Plant CNN Classifier',
        objectives: 'Develop a deep-learning based system capable of identifying medicinal plants from images. Use a convolutional neural network (CNN) to classify plant species based on leaf (or plant) photos, and deliver a tool that can help botanists, researchers or users quickly and accurately recognize medicinal plant types.',
        challenges: [
            'Limited and imbalanced dataset of medicinal plant images',
            'Similar morphological features between different plant species',
            'Variations in lighting, background, and image quality',
            'Achieving high accuracy while maintaining model generalization',
            'Data augmentation strategies for small botanical datasets'
        ],
        learned: [
            'Advanced CNN architectures (ResNet, EfficientNet) for botanical classification',
            'Transfer learning techniques using pre-trained models on ImageNet',
            'Data augmentation specifically for plant images (rotation, color jitter)',
            'Gradient-weighted Class Activation Mapping (Grad-CAM) for model interpretability',
            'Handling class imbalance with weighted loss functions',
            'Deployment of CNN models as REST APIs for easy integration'
        ]
    },
    'safevision': {
        title: 'SafeVision – Industrial Helmet Detection System',
        objectives: 'Implement a computer vision model for helmet detection using deep learning (YOLOv8) with optimized quick training, validation, and real-time inference for workplace safety monitoring.',
        challenges: [
            'Real-time detection with high precision in industrial environments',
            'Handling varying lighting conditions and occlusions',
            'Differentiating between helmets and similar-shaped objects',
            'Optimizing model for edge deployment on resource-constrained devices',
            'Creating robust training dataset with industrial safety scenarios'
        ],
        learned: [
            'YOLOv8 architecture and optimization techniques',
            'Real-time object detection pipeline design',
            'Data annotation and augmentation for safety equipment',
            'Model quantization for edge deployment',
            'Performance metrics for object detection (mAP, IoU, FPS)',
            'Integration with surveillance systems and alert mechanisms'
        ]
    },
    'ai_researcher_course': {
        title: 'Become an AI Researcher Course – Complete Learning Path',
        objectives: 'Design and implement a comprehensive, self-contained curriculum that takes learners from mathematical fundamentals to understanding and implementing modern Large Language Models (LLMs). The course emphasizes building intuition from first principles rather than relying on high-level abstractions.',
        challenges: [
            'Creating intuitive explanations for complex mathematical concepts (derivatives, linear algebra, probability)',
            'Structuring progressive learning that connects theory to implementation seamlessly',
            'Implementing neural network components from scratch without relying on high-level frameworks',
            'Demystifying Transformer architecture and attention mechanisms step-by-step',
            'Ensuring all code examples are educational, optimized, and production-ready for learning'
        ],
        learned: [
            'Curriculum design for technical AI/ML education that bridges theory and practice',
            'The critical mathematical underpinnings of modern deep learning systems',
            'How to implement and visualize backpropagation and optimization algorithms manually',
            'Transformer architecture decomposition: from attention to full model implementation',
            'Teaching complex topics through progressive, hands-on coding exercises'
        ]
    }
};

// ==================== THEME TOGGLE ====================
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
themeToggle.textContent = savedTheme === 'dark' ? '🌙' : '☀️';

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    themeToggle.textContent = newTheme === 'dark' ? '🌙' : '☀️';
});

// ==================== MOBILE MENU ====================
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');

mobileMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Close menu when clicking on a link
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// ==================== SMOOTH SCROLL ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ==================== SCROLL ANIMATIONS ====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// ==================== MODAL FUNCTIONS ====================
function openModal(projectKey) {
    const modal = document.getElementById('projectModal');
    const project = projectData[projectKey];
    
    document.getElementById('modalTitle').textContent = project.title;
    document.getElementById('modalObjectives').textContent = project.objectives;
    
    // Populate challenges
    const challengesList = document.getElementById('modalChallenges');
    challengesList.innerHTML = '';
    project.challenges.forEach(challenge => {
        const li = document.createElement('li');
        li.textContent = challenge;
        challengesList.appendChild(li);
    });
    
    // Populate learned
    const learnedList = document.getElementById('modalLearned');
    learnedList.innerHTML = '';
    project.learned.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        learnedList.appendChild(li);
    });
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('projectModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal on outside click
document.getElementById('projectModal').addEventListener('click', (e) => {
    if (e.target.id === 'projectModal') {
        closeModal();
    }
});

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// ==================== CONTACT FORM ====================
const contactForm = document.getElementById('contactForm');

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
    
    // Get form values
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    
    let isValid = true;
    
    // Validate name
    if (name.length < 2) {
        document.getElementById('nameError').textContent = 'Name must be at least 2 characters';
        isValid = false;
    }
    
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Please enter a valid email';
        isValid = false;
    }
    
    // Validate message
    if (message.length < 10) {
        document.getElementById('messageError').textContent = 'Message must be at least 10 characters';
        isValid = false;
    }
    
    if (isValid) {
        alert('Thank you for your message! This is a demo form. In production, this would send your message.');
        contactForm.reset();
    }
});

// ==================== COPY EMAIL ====================
function copyEmail() {
    const emailText = document.getElementById('emailText');
    emailText.select();
    document.execCommand('copy');
    
    const copyBtn = event.target;
    const originalText = copyBtn.textContent;
    copyBtn.textContent = 'Copied!';
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
    }, 2000);
}




const canvas = document.getElementById("heroCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = document.querySelector(".hero").offsetHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

const particles = [];
const particleCount = 90;

for (let i = 0; i < particleCount; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2 + 1,
        dx: (Math.random() - 0.5) * 0.6,
        dy: (Math.random() - 0.5) * 0.6
    });
}

function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((p, i) => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = "#00f5d4";
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dist = Math.hypot(p.x - p2.x, p.y - p2.y);

            if (dist < 120) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = "rgba(59,130,246,0.2)";
                ctx.stroke();
            }
        }

        p.x += p.dx;
        p.y += p.dy;

        if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
    });

    requestAnimationFrame(drawParticles);
}

drawParticles();


const aboutCanvas = document.getElementById("aboutCanvas");
const aboutCtx = aboutCanvas.getContext("2d");

function resizeAboutCanvas() {
    aboutCanvas.width = window.innerWidth;
    aboutCanvas.height = document.getElementById("about").offsetHeight;
}
resizeAboutCanvas();
window.addEventListener("resize", resizeAboutCanvas);

const blobs = [];

for (let i = 0; i < 8; i++) {
    blobs.push({
        x: Math.random() * aboutCanvas.width,
        y: Math.random() * aboutCanvas.height,
        r: 120 + Math.random() * 80,
        dx: (Math.random() - 0.5) * 0.3,
        dy: (Math.random() - 0.5) * 0.3,
        color: i % 2 === 0
            ? "rgba(0,245,212,0.18)"   // cyan
            : "rgba(168,85,247,0.18)" // purple
    });
}

function drawBlobBackground() {
    aboutCtx.clearRect(0, 0, aboutCanvas.width, aboutCanvas.height);

    blobs.forEach(blob => {
        const grad = aboutCtx.createRadialGradient(
            blob.x, blob.y, 0,
            blob.x, blob.y, blob.r
        );

        grad.addColorStop(0, blob.color);
        grad.addColorStop(1, "transparent");

        aboutCtx.fillStyle = grad;
        aboutCtx.beginPath();
        aboutCtx.arc(blob.x, blob.y, blob.r, 0, Math.PI * 2);
        aboutCtx.fill();

        blob.x += blob.dx;
        blob.y += blob.dy;

        if (blob.x < -blob.r || blob.x > aboutCanvas.width + blob.r) blob.dx *= -1;
        if (blob.y < -blob.r || blob.y > aboutCanvas.height + blob.r) blob.dy *= -1;
    });

    requestAnimationFrame(drawBlobBackground);
}

drawBlobBackground();




// ==================== CONTACT FORM WITH EMAILJS ====================
document.addEventListener("DOMContentLoaded", function () {
    // Initialize EmailJS
    emailjs.init("qnNn4V54YlY7wpPre");

    const contactForm = document.getElementById("contactForm");
  
    if (!contactForm) {
        console.error("Contact form not found!");
        return;
    }

    contactForm.addEventListener("submit", function(e) {
        e.preventDefault();
    
        // Clear previous errors
        document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
    
        // Get form values
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();
    
        let isValid = true;
    
        // Validate name
        if (name.length < 2) {
            document.getElementById('nameError').textContent = 'Name must be at least 2 characters';
            isValid = false;
        }
    
        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('emailError').textContent = 'Please enter a valid email';
            isValid = false;
        }
    
        // Validate message
        if (message.length < 10) {
            document.getElementById('messageError').textContent = 'Message must be at least 10 characters';
            isValid = false;
        }
    
        // If validation passes, send email
        if (isValid) {
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';

            emailjs.send(
                "service_qzedrks",
                "template_4sw0p7a",
                {
                    name: name,
                    email: email,
                    message: message
                }
            )
            .then(() => {
                alert("✅ Message sent successfully!");
                contactForm.reset();
                submitBtn.disabled = false;
                submitBtn.textContent = 'Send Message';
            })
            .catch((error) => {
                alert("❌ Failed to send message! Please try again.");
                console.error("EMAILJS ERROR:", error);
                submitBtn.disabled = false;
                submitBtn.textContent = 'Send Message';
            });
        }
    });
});