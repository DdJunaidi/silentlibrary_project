
// Back to top
const backBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  if (window.scrollY > 400) backBtn?.classList.add('show'); else backBtn?.classList.remove('show');
});
backBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Form validation
(() => {
  'use strict';
  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) { event.preventDefault(); event.stopPropagation(); }
      form.classList.add('was-validated');
    }, false);
  });
})();

// Sample books (placeholder covers)
// const books = Array.from({length: 24}, (_,i)=>{
//   const genres = ['Fiction','Non-fiction','Children','Self-help','Science','History'];
//   const availability = Math.random() > 0.25 ? 'Available' : 'Checked out';
//   return {
//     id: i+1,
//     title: `Sample Book ${i+1}`,
//     author: `Author ${String.fromCharCode(65 + (i%26))}`,
//     genre: genres[i%genres.length],
//     status: availability,
//     cover: `https://picsum.photos/seed/book-${i+1}/600/800`
//   }
// });

// function renderBooks(sliceEnd = 12){
//   const grid = document.getElementById('booksGrid');
//   if(!grid) return;
//   const q = document.getElementById('bookSearch')?.value.toLowerCase() || '';
//   const g = document.getElementById('genreFilter')?.value || '';
//   const a = document.getElementById('availabilityFilter')?.value || '';
//   const filtered = books.filter(b => {
//     const matchQ = b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q);
//     const matchG = g ? b.genre === g : true;
//     const matchA = a ? b.status === a : true;
//     return matchQ && matchG && matchA;
//   }).slice(0, sliceEnd);
//   grid.innerHTML = filtered.map(b => `
//     <div class="col-sm-6 col-md-4 col-lg-3" data-aos="fade-up">
//       <div class="card h-100 rounded-4 book-card hover-card">
//         <img src="${b.cover}" alt="${b.title}" class="card-img-top">
//         <div class="card-body">
//           <div class="d-flex justify-content-between align-items-start">
//             <h5 class="card-title mb-1">${b.title}</h5>
//             <span class="badge ${b.status==='Available'?'text-bg-success':'text-bg-secondary'}">${b.status}</span>
//           </div>
//           <p class="text-muted mb-2">${b.author}</p>
//           <span class="tag">${b.genre}</span>
//         </div>
//       </div>
//     </div>
//   `).join('');
// }

// let booksVisible = 12;
// document.getElementById('bookSearch')?.addEventListener('input', ()=>{ booksVisible=12; renderBooks(booksVisible); });
// document.getElementById('genreFilter')?.addEventListener('change', ()=>{ booksVisible=12; renderBooks(booksVisible); });
// document.getElementById('availabilityFilter')?.addEventListener('change', ()=>{ booksVisible=12; renderBooks(booksVisible); });
// document.getElementById('loadMoreBooks')?.addEventListener('click', ()=>{ booksVisible += 12; renderBooks(booksVisible); });

// // Init filters and grid
// const genreSelect = document.getElementById('genreFilter');
// if (genreSelect && genreSelect.children.length <= 1){
//   [...new Set(books.map(b=>b.genre))].sort().forEach(g=>{
//     const opt = document.createElement('option'); opt.value = g; opt.textContent = g; genreSelect.appendChild(opt);
//   });
// }
// renderBooks(booksVisible);

// Simple events (placeholder images)
const sampleEvents = [
  { id:1, title:'Author Talk: Journey Through Mystery', type:'Talk', date:'2025-09-02', month:9, img:'https://picsum.photos/seed/author-talk/800/600' },
  { id:2, title:'Kids Storytelling Hour', type:'Kids', date:'2025-09-14', month:9, img:'https://picsum.photos/seed/storytime/800/600' },
  { id:3, title:'Creative Writing Workshop', type:'Workshop', date:'2025-10-05', month:10, img:'https://picsum.photos/seed/writing/800/600' },
  { id:4, title:'Book Drive Promotion', type:'Promotion', date:'2025-10-20', month:10, img:'https://picsum.photos/seed/bookdrive/800/600' },
];

function renderMonthOptions(){
  const sel = document.getElementById('eventMonthFilter');
  if(!sel) return;
  const months = [...new Set(sampleEvents.map(e=>e.month))];
  months.sort((a,b)=>a-b).forEach(m=>{
    const opt = document.createElement('option');
    opt.value = m;
    opt.textContent = new Date(2025, m-1, 1).toLocaleString(undefined, { month:'long' });
    sel.appendChild(opt);
  });
}
function renderEvents(){
  const grid = document.getElementById('eventsGrid');
  if(!grid) return;
  const t = document.getElementById('eventTypeFilter')?.value || '';
  const m = document.getElementById('eventMonthFilter')?.value || '';
  const today = new Date().toISOString().slice(0,10);
  const items = sampleEvents.filter(e => (t? e.type===t : true) && (m? String(e.month)===String(m) : true));
  grid.innerHTML = items.map(e => `
    <div class="col-md-6 col-lg-4" data-aos="fade-up">
      <div class="card h-100 rounded-4 hover-card">
        <img src="${e.img}" class="card-img-top" alt="${e.title}">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h5 class="card-title">${e.title}</h5>
            ${e.date >= today ? '<span class="badge text-bg-info">Upcoming</span>' : ''}
          </div>
          <p class="text-muted mb-2">${new Date(e.date).toLocaleDateString(undefined, { day:'2-digit', month:'short', year:'numeric'})}</p>
          <span class="tag">${e.type}</span>
        </div>
      </div>
    </div>
  `).join('');
}
document.getElementById('eventTypeFilter')?.addEventListener('change', renderEvents);
document.getElementById('eventMonthFilter')?.addEventListener('change', renderEvents);
renderMonthOptions(); renderEvents();
