import type { ReactNode } from 'react';
import { ThemeControl } from '@xvadur/ui';
export type ManualPage = 'home' | 'foundations' | 'components' | 'fonts' | 'images';
const chapters = [
  { id: 'home', href: '/', label: 'Domov', group: 'Manuál' },
  { id: 'foundations', href: '/zaklady/', label: 'Základy vizuálu', group: 'Manuál' },
  { id: 'components', href: '/komponenty/', label: 'Komponenty', group: 'Manuál' },
  { id: 'fonts', href: '/fonty/', label: 'Výber písiem', group: 'Pracovné podklady' },
  { id: 'images', href: '/obrazky/', label: 'Fotografie', group: 'Pracovné podklady' },
] as const;
export default function StackHeader({ active, version, children }: { active: ManualPage; version: string; children?: ReactNode }) {
  const current = chapters.find(item => item.id === active)!;
  return <>
    <aside className="manual-sidebar">
      <a href="/" className="manual-brand">XVADUR<span>Dizajnový manuál</span></a>
      <nav aria-label="Obsah manuálu">{['Manuál', 'Pracovné podklady'].map(group => <div className="manual-nav-group" key={group}><p>{group}</p>{chapters.filter(item => item.group === group).map(item => <a key={item.id} href={item.href} aria-current={active === item.id ? 'page' : undefined}>{item.label}</a>)}</div>)}</nav>
      <div className="manual-sidebar-footer"><span>Stack {version} · vo vývoji</span><a href="https://github.com/xvadur/system">GitHub / xvadur/system ↗</a></div>
    </aside>
    <header className="manual-topbar">
      <div className="manual-breadcrumb"><a href="/">XVADUR Stack</a><span aria-hidden="true">/</span><span>{current.label}</span></div>
      <ThemeControl storageKey="xvadur-ui-theme" />
      <label className="manual-mobile-nav">Kapitola manuálu<select aria-label="Kapitola manuálu" value={current.href} onChange={event => { window.location.href = event.target.value; }}>{chapters.map(item => <option key={item.id} value={item.href}>{item.label}</option>)}</select></label>
      {children}
    </header>
  </>;
}
