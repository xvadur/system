import { useState, type ReactNode } from 'react';
import { Button, ActionLink, TextField, TextArea, Badge, Surface, ProjectCard, Notice, EmptyState, Toggle, Accordion, Tabs, Dialog, ThemeControl } from '@xvadur/ui';
import registry from '../../registry.json';

const materials = [{ id: 'flat', label: 'Plochý' }, { id: 'soft', label: 'Plastický' }, { id: 'neumorphic', label: 'Neumorphism' }] as const;

function Example({ id }: { id: string }) {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [open, setOpen] = useState(false);
  const [checked, setChecked] = useState(false);
  switch (id) {
    case 'button': return <div className="example-row"><Button>Hlavný krok</Button><Button variant="secondary">Vedľajší krok</Button><Button variant="ghost">Tichý krok</Button><Button disabled>Nedostupné</Button><Button loading>Ukladanie</Button></div>;
    case 'action-link': return <div className="example-row"><ActionLink href="#installation">Ako ho použiť ↗</ActionLink><ActionLink href="#versions" variant="secondary">Verzie</ActionLink></div>;
    case 'text-field': return <form className="example-form" noValidate onSubmit={event => { event.preventDefault(); const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); setError(valid ? '' : 'Zadaj e-mail v tvare meno@domena.sk.'); setMessage(valid ? 'Tvar adresy sedí. Ukážka nič neodosiela.' : ''); }}><TextField label="E-mail" type="email" value={email} onChange={event => setEmail(event.target.value)} description="Lokálna ukážka validácie." error={error} required /><Button type="submit" variant="secondary">Skontrolovať</Button>{message ? <p role="status">{message}</p> : null}</form>;
    case 'text-area': return <TextArea label="Čo potrebuješ vytvoriť?" description="Text zostáva iba v tejto ukážke." rows={3} placeholder="Opíš konkrétnu vec…" />;
    case 'badge': return <div className="example-row"><Badge>Pracovná verzia</Badge><Badge tone="success">Pripravené</Badge><Badge tone="warning">Vo vývoji</Badge><Badge tone="danger">Vyžaduje opravu</Badge></div>;
    case 'surface': return <Surface className="example-surface"><p className="eyebrow">Zdieľaný povrch</p><h3>Obsah má svoj priestor.</h3><p>Rovnaký komponent v katalógu aj na webe.</p></Surface>;
    case 'project-card': return <ProjectCard href="#installation" title="Prvá integrácia" description="Takto bude vyzerať karta skutočného projektu. Obsah a stav dodáva web." status="Ukážka komponentu" meta="Projekt / 01" />;
    case 'notice': return <div className="example-stack"><Notice tone="neutral" title="Pracovný základ">Verzia kódu a prijatie vzhľadu sú dve odlišné veci.</Notice><Notice tone="danger" title="Nepodarilo sa uložiť">Vyskúšaj krok znova. Tvoje zadanie zostáva zachované.</Notice></div>;
    case 'empty-state': return <><EmptyState title="Zatiaľ tu nič nie je." description="Pridaj prvý komponent do svojho výberu." action={<Button variant="secondary" onClick={() => setMessage('Komponent môžeš vybrať v navigácii katalógu.')}>Vybrať komponent</Button>} />{message ? <p role="status">{message}</p> : null}</>;
    case 'toggle': return <Toggle label="Zobrazovať pomocné popisy" description={checked ? 'Pomocné popisy sú zapnuté.' : 'Pomocné popisy sú vypnuté.'} checked={checked} onChange={event => setChecked(event.target.checked)} />;
    case 'accordion': return <Accordion title="Čo patrí do spoločného komponentu?"><p>Správanie, prístupnosť a opakujúci sa vzhľad. Konkrétne názvy, texty a odkazy zostávajú v obsahu webu.</p></Accordion>;
    case 'tabs': return <Tabs label="Dokumentácia komponentu" items={[{ id: 'usage', label: 'Použitie', content: <p>Importuj komponent z balíčka a odovzdaj mu svoj obsah.</p> }, { id: 'states', label: 'Stavy', content: <p>Skontroluj bežný, zakázaný, načítavací a chybový stav.</p> }, { id: 'keyboard', label: 'Klávesnica', content: <p>Medzi záložkami sa presúvaš šípkami, Home a End.</p> }]} />;
    case 'dialog': return <><Button variant="secondary" onClick={() => setOpen(true)}>Otvoriť dialóg</Button><Dialog open={open} onOpenChange={setOpen} title="Jeden komponent. Rovnaké správanie." description="Toto je natívny modálny dialóg."><p>Escape ho zavrie a fokus sa vráti na pôvodné tlačidlo.</p><Button onClick={() => setOpen(false)}>Rozumiem</Button></Dialog></>;
    case 'theme-control': return <ThemeControl storageKey="xvadur-ui-theme" />;
    default: return <p>Ukážka sa pripravuje.</p>;
  }
}

function Code({ children }: { children: string }) {
  const [result, setResult] = useState('Kopírovať');
  return <div className="code-block"><pre><code>{children}</code></pre><button type="button" className="copy-code" onClick={async () => { try { await navigator.clipboard.writeText(children); setResult('Skopírované'); } catch { setResult('Označ a skopíruj text'); } }} aria-live="polite">{result}</button></div>;
}

function Section({ id, number, title, children }: { id: string; number: string; title: string; children: ReactNode }) {
  return <section id={id} className="catalog-section"><div className="section-heading"><span className="eyebrow">{number}</span><h2>{title}</h2></div>{children}</section>;
}

export default function Catalog({ version }: { version: string }) {
  const [material, setMaterial] = useState('flat');
  const [search, setSearch] = useState('');
  const components = registry.components.filter(item => `${item.name} ${item.description} ${item.category}`.toLocaleLowerCase('sk').includes(search.toLocaleLowerCase('sk')));
  return <>
    <header className="catalog-header"><a href="#main" className="wordmark">XVADUR<span>/ UI</span></a><div className="header-meta"><span>v{version}</span><ThemeControl storageKey="xvadur-ui-theme" /></div><select className="mobile-component-jump" aria-label="Prejsť na komponent" defaultValue="" onChange={event => { if (event.currentTarget.value) window.location.hash = event.currentTarget.value; }}><option value="">Komponenty ({registry.components.length})</option>{registry.components.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></header>
    <aside className="catalog-sidebar"><p className="eyebrow">Pracovná knižnica</p><nav aria-label="Obsah katalógu"><a href="#main">Prehľad</a><a href="#materials">Materiál</a><a href="#tokens">Tokeny</a><a href="#components">Komponenty <span>{registry.components.length}</span></a>{registry.components.map(item => <a className="component-nav" href={`#${item.id}`} key={item.id}>{item.name}</a>)}<a href="#installation">Použitie na webe</a><a href="#versions">Verzie</a></nav><a className="repo-link" href="https://github.com/xvadur/design-system">GitHub ↗</a></aside>
    <main id="main" className="catalog-main">
      <div className="catalog-intro"><p className="eyebrow"><span className="version-dot" /> Zdroj → komponent → web</p><h1>Náš spoločný<br /><em>stavebný základ.</em></h1><p className="intro-copy">Tokeny, komponenty a ich správanie na jednom mieste. To, čo tu skúšaš, je ten istý kód, ktorý importujeme do webu.</p><div className="intro-facts"><span><strong>{registry.components.length}</strong> komponentov</span><span><strong>{version}</strong> prvá pracovná verzia</span><span>React + CSS<br />Astro katalóg</span></div></div>
      <Section id="materials" number="01" title="Ako pôsobí povrch"><p className="section-description">Vzhľad môžeme posúdiť na rovnakých komponentoch. Plastický štýl a neumorphism sú experimentálne možnosti; prepnutie v katalógu neznamená prijatie smeru.</p><div className="material-picker" role="group" aria-label="Materiál komponentov">{materials.map(item => <Button key={item.id} variant={material === item.id ? 'primary' : 'secondary'} aria-pressed={material === item.id} onClick={() => { setMaterial(item.id); document.documentElement.dataset.material = item.id; }}>{item.label}</Button>)}</div><Surface className="material-preview"><TextField label="Názov projektu" defaultValue="XVADUR" /><div className="example-row"><Button>Otvoriť projekt</Button><Button variant="secondary">Upraviť</Button><Toggle label="Zobraziť detail" /></div></Surface></Section>
      <Section id="tokens" number="02" title="Spoločné hodnoty"><p className="section-description">Farby, písmo, rozmery a pohyb majú pomenované CSS premenné. Pri zmene tokenu sa aktualizujú všetky jeho použitia.</p><div className="swatches">{[{ name: 'Pozadie', token: '--xv-bg' }, { name: 'Povrch', token: '--xv-surface' }, { name: 'Text', token: '--xv-text' }, { name: 'Hlavná akcia', token: '--xv-accent' }, { name: 'Fokus', token: '--xv-focus' }].map(item => <div className="swatch" key={item.token}><span style={{ background: `var(${item.token})` }} /><strong>{item.name}</strong><code>{item.token}</code></div>)}</div><Code>{"import '@xvadur/ui/tokens.css';\nimport '@xvadur/ui/styles.css';\n// Voliteľné vložené fonty:\nimport '@xvadur/ui/fonts.css';"}</Code></Section>
      <Section id="components" number="03" title="Skutočné komponenty"><TextField label="Nájsť komponent" type="search" value={search} onChange={event => setSearch(event.target.value)} placeholder="Napríklad Button alebo dialóg" /><p className="search-result" role="status">{components.length} z {registry.components.length} komponentov</p>{components.length ? components.map(item => <article id={item.id} className="component-entry" key={item.id}><div className="component-title"><div><p className="eyebrow">{item.category}</p><h3>{item.name}</h3></div><Badge>od {item.since}</Badge></div><p className="component-description">{item.description}</p><div className="live-example"><Example id={item.id} /></div><details className="source-details"><summary>Použitie a zdroj</summary><Code>{`import { ${item.name} } from '@xvadur/ui';\n\n${item.example}`}</Code><p><code>{item.source}</code> · stav: pracovná verzia</p></details></article>) : <EmptyState title="Taký komponent tu zatiaľ nie je." action={<Button variant="secondary" onClick={() => setSearch('')}>Zobraziť všetky</Button>} />}</Section>
      <Section id="installation" number="04" title="Z katalógu do webu"><p className="section-description">Web si pripne konkrétny Git tag. Nová verzia knižnice sa doň dostane vedomou aktualizáciou závislosti.</p><Code>{`npm install 'git+https://github.com/xvadur/design-system.git#v${version}'`}</Code><p className="section-description">V Astro môže byť bežný komponent vykreslený na serveri. Interaktívny komponent dostane hydratáciu cez <code>client:load</code>.</p><Code>{`---\nimport { ActionLink } from '@xvadur/ui';\nimport '@xvadur/ui/tokens.css';\nimport '@xvadur/ui/styles.css';\n---\n<ActionLink href="/projekty/">Preskúmať projekty</ActionLink>`}</Code></Section>
      <Section id="versions" number="05" title="Rastie spolu s nami"><div className="version-panel"><Badge>v{version}</Badge><h3>Prvý použiteľný základ.</h3><p>Zdrojový kód, typy, tokeny a tento katalóg sa vyvíjajú spolu. Každý nový komponent dostane ukážku, testy a záznam zmeny.</p><ol><li>Upravíme alebo pridáme komponent.</li><li>Skontrolujeme jeho použitie a stavy.</li><li>Zapíšeme zmenu a zvýšime verziu.</li><li>Web aktualizujeme na nový tag.</li></ol><ActionLink href="https://github.com/xvadur/design-system" variant="secondary">Otvoriť repozitár ↗</ActionLink></div></Section>
      <footer className="catalog-footer"><strong>XVADUR / UI</strong><span>Pracovný systém · v{version} · Adam Rudavský</span></footer>
    </main>
  </>;
}
