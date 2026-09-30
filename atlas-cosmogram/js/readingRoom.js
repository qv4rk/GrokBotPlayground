/**
 * Reading Room — sliding drawer over blurred canvas.
 */

export class ReadingRoom {
  constructor(rootEl) {
    this.root = rootEl;
    this.titleEl = rootEl.querySelector('[data-rr-title]');
    this.metaEl = rootEl.querySelector('[data-rr-meta]');
    this.excerptEl = rootEl.querySelector('[data-rr-excerpt]');
    this.closeBtn = rootEl.querySelector('[data-rr-close]');
    this.backdrop = document.getElementById('rr-backdrop');
    this.canvas = document.getElementById('globe-canvas');

    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.close());
    }
    if (this.backdrop) {
      this.backdrop.addEventListener('click', () => this.close());
    }
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen()) this.close();
    });
  }

  isOpen() {
    return this.root.classList.contains('open');
  }

  open(article) {
    if (!article) return;
    if (this.titleEl) this.titleEl.textContent = article.title || '';
    if (this.metaEl) {
      const year = article.year;
      const era = year < 1 ? 'BCE' : 'CE';
      const yDisp = year < 1 ? 1 - year : year;
      const place = article.place || '';
      this.metaEl.textContent = `${yDisp} ${era}${place ? ' · ' + place : ''}`;
    }
    if (this.excerptEl) this.excerptEl.textContent = article.excerpt || '';
    this.root.classList.add('open');
    this.root.setAttribute('aria-hidden', 'false');
    if (this.backdrop) this.backdrop.classList.add('visible');
    if (this.canvas) this.canvas.classList.add('blurred');
  }

  close() {
    this.root.classList.remove('open');
    this.root.setAttribute('aria-hidden', 'true');
    if (this.backdrop) this.backdrop.classList.remove('visible');
    if (this.canvas) this.canvas.classList.remove('blurred');
  }
}

export default ReadingRoom;
