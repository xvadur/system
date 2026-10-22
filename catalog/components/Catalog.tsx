import { useState, type ReactNode } from 'react';
import { Button, ActionLink, TextField, TextArea, Badge, Surface, ProjectCard, Notice, EmptyState, Toggle, Accordion, Tabs, Dialog, ThemeControl } from '@xvadur/ui';
import registry from '../../registry.json';


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

function Section({ id, title, children }: { id: string; title: string; children: ReactNode }) {
  return <section id={id} className="catalog-section"><div className="section-heading"><h2>{title}</h2></div>{children}</section>;
}

export default function Catalog({ version }: { version: string }) {
  const [search, setSearch] = useState('');
  const components = registry.components.filter(item => `${item.name} ${item.description} ${item.category}`.toLocaleLowerCase('sk').includes(search.toLocaleLowerCase('sk')));
  return <>
    <div className="manual-catalog" data-material="neumorphic">
      <header className="manual-page-heading" id="main"><h1>Komponenty</h1><p>Živé príklady spoločných prvkov. Každý má popísané správanie, varianty a zdroj; finálny vizuál ešte dolaďujeme.</p></header>
      <nav className="manual-page-outline" aria-label="Komponenty">{registry.components.map(item => <a href={`#${item.id}`} key={item.id}>{item.name}</a>)}</nav>
      <Section id="components" title="Katalóg prvkov"><TextField label="Nájsť komponent" type="search" value={search} onChange={event => setSearch(event.target.value)} placeholder="Napríklad Button alebo dialóg" /><p className="search-result" role="status">{components.length} z {registry.components.length} komponentov</p>{components.length ? components.map(item => <article id={item.id} className="component-entry" key={item.id}><div className="component-title"><div><p className="component-category">{item.category}</p><h3>{item.name}</h3></div><Badge>od {item.since}</Badge></div><p className="component-description">{item.description}</p><div className="live-example"><Example id={item.id} /></div><details className="source-details"><summary>Použitie a zdroj</summary><Code>{`import { ${item.name} } from '@xvadur/ui';\n\n${item.example}`}</Code><p><code>{item.source}</code> · stav: pracovná verzia</p></details></article>) : <EmptyState title="Taký komponent tu zatiaľ nie je." action={<Button variant="secondary" onClick={() => setSearch('')}>Zobraziť všetky</Button>} />}</Section>
      <Section id="installation" title="Z katalógu do webu"><p className="section-description">Zdroj a brand book sú v repozitári xvadur/system. Pri verziovanom vydaní si spotrebiteľ pripne konkrétny Git tag; prvý release tag ešte pripravíme.</p><Code>{`npm install 'git+https://github.com/xvadur/system.git#v${version}'`}</Code><p className="section-description">V Astro môže byť bežný komponent vykreslený na serveri. Interaktívny komponent dostane hydratáciu cez <code>client:load</code>.</p><Code>{`---\nimport { ActionLink } from '@xvadur/ui';\nimport '@xvadur/ui/tokens.css';\nimport '@xvadur/ui/styles.css';\n---\n<ActionLink href="/projekty/">Preskúmať projekty</ActionLink>`}</Code></Section>
      <Section id="versions" title="Rastie spolu s nami"><div className="version-panel"><Badge>v{version}</Badge><h3>Prvý použiteľný základ.</h3><p>Zdrojový kód, typy, tokeny a tento katalóg sa vyvíjajú spolu. Každý nový komponent dostane ukážku, testy a záznam zmeny.</p><ol><li>Upravíme alebo pridáme komponent.</li><li>Skontrolujeme jeho použitie a stavy.</li><li>Zapíšeme zmenu a zvýšime verziu.</li><li>Web aktualizujeme na nový tag.</li></ol><ActionLink href="https://github.com/xvadur/system" variant="secondary">Otvoriť repozitár ↗</ActionLink></div></Section>
    </div>
  </>;
}
