import type { ReactNode } from 'react';
import { ThemeControl } from '@xvadur/ui';

export default function StackHeader({ active, version, children }: { active: 'language' | 'components' | 'fonts' | 'images'; version: string; children?: ReactNode }) {
  return <header className="catalog-header stack-header">
    <a href="/" className="wordmark">XVADUR<span>Stack / Brand book</span></a>
    <nav className="stack-navigation" aria-label="XVADUR Stack">
      <a href="/" aria-current={active === 'language' ? 'page' : undefined}>Design language</a>
      <a href="/komponenty/" aria-current={active === 'components' ? 'page' : undefined}>Komponenty a tokeny</a>
      <a href="/fonty/" aria-current={active === 'fonts' ? 'page' : undefined}>Fonty</a>
      <a href="/obrazky/" aria-current={active === 'images' ? 'page' : undefined}>Fotky</a>
    </nav>
    <div className="header-meta"><span>Pracovná verzia · {version}</span><ThemeControl storageKey="xvadur-ui-theme" /></div>
    {children}
  </header>;
}
