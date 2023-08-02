let scrollDirection = 1;


const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray;
let originalNumberOfParticles;

// Get mouse position
let mouse = {
  x: null,
  y: null,
  radius: (canvas.height/80) * (canvas.width/80)
};

window.addEventListener('mousemove', function(event) {
  mouse.x = event.x;
  mouse.y = event.y;
});

// Create particles
class Particle {
  constructor(x, y, directionX, directionY, size, color) {
    this.x = x;
    this.y = y;
    this.directionX = directionX;
    this.directionY = directionY;
    this.size = size;
    this.color = color;
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
    ctx.fillStyle = this.color;
    ctx.fill();
  }
  update() {
    if (this.x + this.size > canvas.width || this.x - this.size < 0) {
      this.directionX = -this.directionX;
    }
    if (this.y + this.size > canvas.height || this.y - this.size < 0) {
      this.directionY = -this.directionY;
    }
    this.x += this.directionX * scrollDirection; // Apply scroll direction
    this.y += this.directionY * scrollDirection; // Apply scroll direction
    // Check distance with other particles
    for (let i = 0; i < particlesArray.length; i++) {
        if (this !== particlesArray[i]) {
        let dx = this.x - particlesArray[i].x;
        let dy = this.y - particlesArray[i].y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        let maxDistance = 100; // Adjust this value to control the distance at which lines are drawn

        if (distance < maxDistance) {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'; // Line color, you can adjust
            ctx.lineWidth = .02 * distance; // Line width, you can adjust
            ctx.beginPath();
            ctx.moveTo(this.x, this.y);
            ctx.lineTo(particlesArray[i].x, particlesArray[i].y);
            ctx.stroke();
        }
        }
    }

    this.draw();
  }  
}

// Create particle array
function init() {
  particlesArray = [];
  originalNumberOfParticles = (canvas.height * canvas.width) / 9000;
  for (let i = 0; i < originalNumberOfParticles; i++) {
    let size = (Math.random() * 5) + 1;
    let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
    let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
    let directionX = (Math.random() * 3) - 1.5;
    let directionY = (Math.random() * 3) - 1.5;
    let color = 'rgba(255, 255, 255, 0.8)';

    particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
  }
}

// Animate particles
function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, innerWidth, innerHeight);

  for (let i = 0; i < particlesArray.length; i++) {
    particlesArray[i].update();
  }
}

// Resize event
window.addEventListener('resize', function() {
  canvas.width = innerWidth;
  canvas.height = innerHeight;
  init();
});

let lastScrollTop = 0;

window.addEventListener('scroll', function() {
  let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  let scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  let scrollPercent = scrollTop / scrollHeight;
  let targetParticles = Math.max(Math.floor((1 - scrollPercent) * originalNumberOfParticles), 0);

  if (scrollTop > lastScrollTop) {
    // Downward scrolling
    scrollDirection = 1;
  } else {
    // Upward scrolling
    scrollDirection = -1;
  }
  lastScrollTop = scrollTop;

  while (particlesArray.length > targetParticles) {
    particlesArray.pop(); // Remove particles from the end
  }
  while (particlesArray.length < targetParticles) {
    let size = (Math.random() * 5) + 1;
    let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
    let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
    let directionX = (Math.random() * 3) - 1.5;
    let directionY = (Math.random() * 3) - 1.5;
    let color = 'rgba(255, 255, 255, 0.8)';
  
    particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
  }
  

});


init();
animate();
