#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Localized GitHub READMEs generated from one public catalogue.

Titles of individual datasets remain the recorded English names to preserve
source traceability; translations are applied only to navigation and editorial
text. No new data, citations or downloads are created by localization.
"""
from collections import Counter

LANGUAGE_LINKS = (
    ('简体中文', 'README.md'), ('English', 'README_EN.md'),
    ('日本語', 'README_JA.md'), ('한국어', 'README_KO.md'),
    ('Español', 'README_ES.md'), ('Deutsch', 'README_DE.md'),
    ('Français', 'README_FR.md'),
)

def language_nav():
    return '🌐 **语言 / Languages:** ' + ' · '.join('[%s](%s)' % (label, path) for label, path in LANGUAGE_LINKS) + '\n\n'

# Translation strings are maintained here; catalogue entries and counts remain
# owned by data/datasets.json and data/catalog_info.json.
LOCALES = {
'JA': {
    'title': '公開バッテリーデータセット・研究リソース集',
    'intro': 'SOC・SOH推定、残存寿命予測、故障診断、安全性、急速充電、実車データなどの研究向け公開情報を整理した索引です。',
    'summary': '{n} 件のリソース · {datasets} 件のデータセット · {portals} 件のポータル + {tools} 件のツール · {papers} 件の論文・目録記録 · {relations} 件のデータ／文献関連付け',
    'scope': '本リポジトリは**メタデータ、解説、リンクのみ**を公開します。第三者の実験生データは保存・再配布しません。取得条件とライセンスは元の提供機関に従ってください。すべてのリンクの現在の有効性を確認したわけではありません。目録基準日: **{date}**。',
    'shortcuts': [('研究分野', 'docs/TOPICS.md'), ('全リソースの詳細', 'docs/DATASET_DETAILS.md'), ('関連文献', 'docs/PAPERS.md'), ('出典と利用上の注意', 'NOTICE.md'), ('2026年の追加分', 'docs/RESEARCH_EXPANSION_20261107.md'), ('CSVデータ', 'data/datasets.csv')],
    'online': 'V2研究ワークベンチ（オンライン）', 'setup': 'GitHub Pages設定ガイド',
    'online_notice': 'GitHub Pages が有効になっていない場合、オンラインページは表示されません。',
    'how_title': '使い方', 'how': [
        'SOC、SOH、RUL などの研究タグ、または機関名を使って対象データを探します。',
        '「データへのアクセス」から元の配布先を開きます。直接ダウンロードではなく案内ページや申請フォームの場合もあります。',
        '研究に利用する前に、原論文、測定条件、版数、ライセンス、取得条件を確認してください。'
    ],
    'directory_title': 'リソース一覧（全件）',
    'headers': ['番号','データセット／リソース','機関','年','種類','研究タグ','データへのアクセス','関連文献'],
    'types': {'dataset':'データセット','portal':'データポータル','tool':'ツール'}, 'access':'アクセス',
    'topic_title': '研究テーマから探す', 'topic_headers':['タグ','件数','研究テーマ'],
    'topics': {'SOC':'充電状態（SOC）の推定','SOH':'健康状態（SOH）の推定','RUL':'残存寿命予測','EIS':'電気化学インピーダンス分光法','FAST':'急速充電','FIELD':'実車・現場計測データ','MODEL':'バッテリーモデリング','SAFETY':'安全性・故障診断'},
    'topic_note':'研究タグは重複します。タグは目録上の分類であり、すべての原データに特定の測定項目があることを保証しません。',
    'caveats_title':'収録範囲と注意事項',
    'caveats': [
        '{n} 件には {datasets} 件のデータセットと {portals} 件のポータル、{tools} 件のツールが含まれます。すべてが独立した実験データではありません。',
        '{papers} 件は論文・データ記録などの目録項目であり、すべてが査読論文ではありません。{relations} 件の関連付けにも確認状況の差があります。',
        '各データセット名は原情報への追跡性のため英語表記を維持しています。詳細ページは主に中国語、一部英語です。',
        'ライセンス、ダウンロード可能性、原データの完全性は一律に確認していません。必ず元の配布元を参照してください。'
    ],
    'maintenance_title':'更新と貢献',
    'maintenance':'本一覧は ADV·BATTERY の単一目録から生成されます。修正・追加提案は [貢献ガイド](CONTRIBUTING.md) を参照してください。[多言語化の方針](docs/I18N.md)と[更新手順](docs/MAINTENANCE.md)もご利用ください。',
},
'KO': {
    'title': '공개 배터리 데이터셋 및 연구 자료 모음',
    'intro': 'SOC/SOH 추정, 잔여수명 예측, 고장 진단, 배터리 안전, 급속 충전 및 실제 차량 운행 데이터 연구를 위한 공개 자료 색인입니다.',
    'summary': '자료 {n}개 · 데이터셋 {datasets}개 · 데이터 포털 {portals}개 + 도구 {tools}개 · 논문/카탈로그 기록 {papers}개 · 데이터–문헌 연결 {relations}개',
    'scope': '이 저장소는 **메타데이터, 설명 및 원본 링크만** 제공합니다. 제3자 실험 원본 데이터를 저장하거나 재배포하지 않습니다. 다운로드 조건과 라이선스는 원 제공 기관의 정책을 따릅니다. 모든 링크의 현재 접근 가능 여부가 검증된 것은 아닙니다. 카탈로그 기준일: **{date}**.',
    'shortcuts': [('연구 분야', 'docs/TOPICS.md'), ('전체 자료 상세', 'docs/DATASET_DETAILS.md'), ('관련 문헌', 'docs/PAPERS.md'), ('출처 및 이용 안내', 'NOTICE.md'), ('2026년 신규 자료', 'docs/RESEARCH_EXPANSION_20261107.md'), ('CSV 데이터', 'data/datasets.csv')],
    'online':'V2 연구 워크벤치 (온라인)', 'setup':'GitHub Pages 설정 안내',
    'online_notice':'GitHub Pages가 활성화되어 있지 않으면 온라인 사이트가 열리지 않습니다.',
    'how_title':'사용 방법', 'how': [
        'SOC, SOH, RUL 등 연구 태그나 기관명으로 필요한 자료를 찾습니다.',
        '"원본 데이터" 링크를 열어 제공 기관의 페이지로 이동합니다. 직접 다운로드 링크가 아닐 수 있습니다.',
        '연구에 활용하기 전 원 논문, 실험 조건, 버전, 라이선스 및 접근 조건을 확인하세요.'
    ],
    'directory_title':'전체 자료 목록',
    'headers':['번호','데이터셋 / 자료','기관','연도','유형','연구 태그','원본 데이터','관련 문헌'],
    'types':{'dataset':'데이터셋','portal':'데이터 포털','tool':'도구'},'access':'접속',
    'topic_title':'연구 주제별 탐색','topic_headers':['태그','자료 수','연구 분야'],
    'topics':{'SOC':'충전 상태(SOC) 추정','SOH':'건강 상태(SOH) 추정','RUL':'잔여 사용 수명 예측','EIS':'전기화학 임피던스 분광법','FAST':'급속 충전','FIELD':'실차 및 현장 데이터','MODEL':'배터리 모델링','SAFETY':'안전 및 고장 진단'},
    'topic_note':'하나의 자료에 여러 태그가 있을 수 있습니다. 태그는 카탈로그 분류이며 원본 데이터의 모든 측정 필드를 검증한 결과는 아닙니다.',
    'caveats_title':'범위 및 유의 사항',
    'caveats':[
        '전체 {n}개 자료에는 데이터셋 {datasets}개, 포털 {portals}개, 도구 {tools}개가 포함되며 모두 독립 실험 데이터는 아닙니다.',
        '문헌/카탈로그 기록 {papers}개가 모두 동료 심사 논문은 아니며, 연결 관계 {relations}개의 검증 수준도 서로 다릅니다.',
        '출처 추적을 위해 데이터셋 이름은 영문으로 유지했습니다. 상세 문서는 주로 중국어이며 일부 영어를 포함합니다.',
        '라이선스, 다운로드 가능 여부 및 원본 파일의 완전성을 일괄 검증하지 않았으므로 공식 출처를 확인하세요.'
    ],
    'maintenance_title':'기여 및 유지 관리',
    'maintenance':'이 목록은 ADV·BATTERY의 단일 카탈로그에서 생성됩니다. 수정 또는 신규 자료 제안은 [기여 안내](CONTRIBUTING.md)를 참고하세요. [다국어 관리 정책](docs/I18N.md) 및 [유지 관리 안내](docs/MAINTENANCE.md)도 확인할 수 있습니다.',
},
'ES': {
    'title':'Colección abierta de datos y recursos de investigación sobre baterías',
    'intro':'Índice de recursos públicos para estimación de SOC y SOH, predicción de vida útil, diagnóstico de fallos, seguridad, carga rápida y datos de conducción real.',
    'summary':'{n} recursos · {datasets} conjuntos de datos · {portals} portales + {tools} herramienta(s) · {papers} registros bibliográficos/de catálogo · {relations} relaciones datos–publicaciones',
    'scope':'Este repositorio publica **metadatos, descripciones y enlaces**, no archivos experimentales de terceros. Las condiciones de acceso y las licencias dependen de cada proveedor. **No se ha comprobado la disponibilidad actual de todos los enlaces.** Fecha de referencia: **{date}**.',
    'shortcuts':[('Temas de investigación','docs/TOPICS.md'),('Fichas detalladas','docs/DATASET_DETAILS.md'),('Publicaciones','docs/PAPERS.md'),('Fuentes y condiciones','NOTICE.md'),('Ampliación 2026','docs/RESEARCH_EXPANSION_20261107.md'),('Datos CSV','data/datasets.csv')],
    'online':'Banco de trabajo V2 (en línea)', 'setup':'Configuración de GitHub Pages',
    'online_notice':'La página pública requiere que GitHub Pages esté habilitado.',
    'how_title':'Cómo utilizar el catálogo','how':[
        'Busque por institución o por etiquetas de investigación como SOC, SOH y RUL.',
        'Abra el enlace «Acceso a los datos» para visitar la fuente original; puede ser una página informativa o requerir autorización.',
        'Antes de usar un conjunto de datos, compruebe el artículo asociado, los protocolos, la versión, la licencia y las condiciones de acceso.'
    ],
    'directory_title':'Catálogo completo de recursos',
    'headers':['N.º','Conjunto de datos / recurso','Institución','Año','Tipo','Etiquetas','Acceso a los datos','Referencia asociada'],
    'types':{'dataset':'Conjunto de datos','portal':'Portal de datos','tool':'Herramienta'},'access':'Acceder',
    'topic_title':'Explorar por área de investigación','topic_headers':['Etiqueta','Recursos','Área de investigación'],
    'topics':{'SOC':'Estimación del estado de carga','SOH':'Estimación del estado de salud','RUL':'Predicción de la vida útil restante','EIS':'Espectroscopia de impedancia electroquímica','FAST':'Carga rápida','FIELD':'Datos de vehículos y operaciones reales','MODEL':'Modelado de baterías','SAFETY':'Seguridad y diagnóstico de fallos'},
    'topic_note':'Las categorías no son excluyentes y no implican que todos los archivos de origen incluyan una variable de medida determinada.',
    'caveats_title':'Alcance y limitaciones',
    'caveats':[
        'Los {n} recursos incluyen {datasets} conjuntos de datos, {portals} portales y {tools} herramienta(s); no representan {n} experimentos independientes.',
        'Los {papers} registros incluyen artículos, reseñas y fichas de datos; no todos son artículos revisados por pares. Las {relations} relaciones tienen distintos niveles de verificación.',
        'Los nombres individuales se conservan en inglés para facilitar la búsqueda de la fuente. Las fichas detalladas están principalmente en chino, con algo de contenido en inglés.',
        'No se garantiza la vigencia de los enlaces, la integridad de los archivos originales ni la validez jurídica de las licencias registradas.'
    ],
    'maintenance_title':'Contribuciones y mantenimiento',
    'maintenance':'Este README se genera a partir de un catálogo único de ADV·BATTERY. Para corregir errores o sugerir recursos, consulte [CONTRIBUTING](CONTRIBUTING.md), la [política de idiomas](docs/I18N.md) y las [instrucciones de mantenimiento](docs/MAINTENANCE.md).',
},
'DE': {
    'title':'Offene Batterie-Datensätze und Forschungsressourcen',
    'intro':'Kuratierter Wegweiser zu öffentlichen Quellen für SOC-/SOH-Schätzung, Lebensdauerprognose, Fehlerdiagnose, Batteriesicherheit, Schnellladen und reale Fahrdaten.',
    'summary':'{n} Ressourcen · {datasets} Datensätze · {portals} Datenportale + {tools} Tool(s) · {papers} Publikations-/Katalogeinträge · {relations} Daten–Literatur-Verknüpfungen',
    'scope':'Dieses Repository enthält **Metadaten, Beschreibungen und Quellenlinks**, keine Rohdaten Dritter. Zugang, Nutzung und Lizenzen richten sich nach den jeweiligen Originalanbietern. **Nicht alle Links wurden aktuell einzeln auf Erreichbarkeit geprüft.** Katalogstand: **{date}**.',
    'shortcuts':[('Forschungsthemen','docs/TOPICS.md'),('Details zu allen Ressourcen','docs/DATASET_DETAILS.md'),('Publikationen','docs/PAPERS.md'),('Quellen und Nutzungsbedingungen','NOTICE.md'),('Erweiterung 2026','docs/RESEARCH_EXPANSION_20261107.md'),('CSV-Daten','data/datasets.csv')],
    'online':'V2-Forschungsoberfläche (online)', 'setup':'GitHub-Pages-Anleitung',
    'online_notice':'Die Online-Seite ist nur erreichbar, wenn GitHub Pages aktiviert wurde.',
    'how_title':'So nutzen Sie das Verzeichnis','how':[
        'Suchen Sie nach Institutionen oder Forschungsmarkierungen wie SOC, SOH und RUL.',
        'Öffnen Sie den Link „Datenzugang“. Er kann zu einer Projektseite oder einem anmeldepflichtigen Portal statt zu einer direkt herunterladbaren Datei führen.',
        'Prüfen Sie vor der Verwendung die Originalpublikation, Versuchsbedingungen, Version, Lizenz und Zugangsbedingungen.'
    ],
    'directory_title':'Vollständiges Ressourcenverzeichnis',
    'headers':['Nr.','Datensatz / Ressource','Institution','Jahr','Typ','Forschungsthemen','Datenzugang','Zugehörige Referenz'],
    'types':{'dataset':'Datensatz','portal':'Datenportal','tool':'Werkzeug'},'access':'Öffnen',
    'topic_title':'Nach Forschungsthema durchsuchen','topic_headers':['Tag','Anzahl','Forschungsthema'],
    'topics':{'SOC':'Ladezustandsschätzung (SOC)','SOH':'Gesundheitszustandsschätzung (SOH)','RUL':'Restlebensdauerprognose','EIS':'Elektrochemische Impedanzspektroskopie','FAST':'Schnellladen','FIELD':'Reale Fahrzeug- und Betriebsdaten','MODEL':'Batteriemodellierung','SAFETY':'Sicherheit und Fehlerdiagnose'},
    'topic_note':'Eine Ressource kann mehreren Kategorien zugeordnet sein. Die Markierungen belegen nicht, dass alle Rohdateien bestimmte Messgrößen enthalten.',
    'caveats_title':'Abdeckung und Einschränkungen',
    'caveats':[
        'Die {n} Ressourcen bestehen aus {datasets} Datensätzen, {portals} Portalen und {tools} Tool(s); sie stehen nicht für {n} unabhängige Experimente.',
        'Die {papers} Publikations-/Katalogeinträge sind nicht ausschließlich begutachtete Artikel. Der Prüfstatus der {relations} Daten–Literatur-Verknüpfungen ist unterschiedlich.',
        'Datensatztitel bleiben zur Nachverfolgbarkeit in der dokumentierten englischen Form. Detailseiten sind überwiegend chinesisch, teilweise englisch.',
        'Downloadverfügbarkeit, Vollständigkeit und Lizenzangaben wurden nicht für jede Quelle unabhängig bestätigt. Maßgeblich ist die Originalquelle.'
    ],
    'maintenance_title':'Mitwirken und Aktualisieren',
    'maintenance':'Diese README-Datei wird aus einem gemeinsamen ADV·BATTERY-Katalog erzeugt. Korrekturen und Vorschläge: [Beitragshinweise](CONTRIBUTING.md), [Sprachpflege](docs/I18N.md) und [Wartungsanleitung](docs/MAINTENANCE.md).',
},
'FR': {
    'title':'Catalogue ouvert de jeux de données et de ressources sur les batteries',
    'intro':'Répertoire de sources publiques pour l’estimation SOC/SOH, la prédiction de durée de vie, le diagnostic de défauts, la sécurité, la charge rapide et les données de conduite réelle.',
    'summary':'{n} ressources · {datasets} jeux de données · {portals} portails + {tools} outil(s) · {papers} notices bibliographiques/de catalogue · {relations} liens données–publications',
    'scope':'Ce dépôt publie **des métadonnées, descriptions et liens**, et non les fichiers expérimentaux bruts de tiers. Les conditions d’accès et licences dépendent des organismes fournisseurs. **La disponibilité de tous les liens n’a pas été vérifiée individuellement à ce jour.** État du catalogue : **{date}**.',
    'shortcuts':[('Thématiques','docs/TOPICS.md'),('Fiches détaillées','docs/DATASET_DETAILS.md'),('Publications','docs/PAPERS.md'),('Sources et conditions','NOTICE.md'),('Ajouts 2026','docs/RESEARCH_EXPANSION_20261107.md'),('Données CSV','data/datasets.csv')],
    'online':'Espace de recherche V2 (en ligne)', 'setup':'Configurer GitHub Pages',
    'online_notice':'Le site en ligne nécessite l’activation préalable de GitHub Pages.',
    'how_title':'Mode d’emploi','how':[
        'Recherchez un organisme ou un thème comme SOC, SOH ou RUL.',
        'Ouvrez le lien « Accès aux données » vers l’hébergeur d’origine ; il peut conduire à une notice ou à une procédure d’accès restreint.',
        'Avant toute utilisation scientifique, vérifiez la publication associée, le protocole, la version, la licence et les conditions d’accès.'
    ],
    'directory_title':'Catalogue complet des ressources',
    'headers':['N°','Jeu de données / ressource','Organisme','Année','Type','Thèmes','Accès aux données','Référence associée'],
    'types':{'dataset':'Jeu de données','portal':'Portail de données','tool':'Outil'},'access':'Accéder',
    'topic_title':'Explorer par thématique','topic_headers':['Tag','Ressources','Thématique'],
    'topics':{'SOC':'Estimation de l’état de charge','SOH':'Estimation de l’état de santé','RUL':'Prédiction de durée de vie restante','EIS':'Spectroscopie d’impédance électrochimique','FAST':'Recharge rapide','FIELD':'Données de véhicules et du terrain','MODEL':'Modélisation de batteries','SAFETY':'Sécurité et diagnostic de défauts'},
    'topic_note':'Une ressource peut relever de plusieurs thèmes. Les étiquettes du catalogue ne prouvent pas la présence d’une variable mesurée dans chaque fichier source.',
    'caveats_title':'Périmètre et limites',
    'caveats':[
        'Les {n} ressources comprennent {datasets} jeux de données, {portals} portails et {tools} outil(s), et non {n} expériences indépendantes.',
        'Les {papers} notices incluent publications, synthèses et fiches de données ; toutes ne correspondent pas à des articles évalués par les pairs. Les {relations} liens n’ont pas tous le même statut de vérification.',
        'Les titres des jeux de données restent dans leur forme anglaise documentée pour faciliter la traçabilité. Les fiches détaillées sont principalement en chinois, parfois en anglais.',
        'Les licences, les possibilités de téléchargement et l’intégrité des données originales n’ont pas toutes fait l’objet d’une vérification indépendante.'
    ],
    'maintenance_title':'Contribuer et maintenir',
    'maintenance':'Ce fichier est généré à partir d’un catalogue ADV·BATTERY unique. Pour proposer une correction ou un ajout, voir le [guide de contribution](CONTRIBUTING.md), la [politique linguistique](docs/I18N.md) et le [guide de maintenance](docs/MAINTENANCE.md).',
},
}

def render_localized_readme(ds, ps, rs, locale, snapshot_date,
                            *, md, disp, link, tags_text, primary_paper,
                            tags_order):
    """Create a full, link-preserving localized catalogue with 1 row per entry."""
    t=LOCALES[locale]
    n=len(ds)
    types=Counter(x['resource_type'] for x in ds)
    tags=Counter(tag for d in ds for tag in d['research_tags'])
    bypaper={p['id']:p for p in ps}
    context={'n':n,'datasets':types['dataset'],'portals':types['portal'],
             'tools':types['tool'],'papers':len(ps),'relations':len(rs),'date':snapshot_date}
    out=['# ADV·BATTERY | '+t['title'],'',language_nav().rstrip(),'','**'+t['intro']+'**','',
         '**'+t['summary'].format(**context)+'**','',
         '> '+t['scope'].format(**context),
         '',
         ' · '.join('[%s](%s)' % (label,path) for label,path in t['shortcuts']),'',
         '**[%s](https://jimjury.github.io/ADV-BATTERY-Dataset-Collection/)** · [%s](docs/GITHUB_V2_LINK_SETUP.md)' % (t['online'],t['setup']),
         '',t['online_notice'],'',
         '## '+t['how_title'],'']
    out.extend('%d. %s' % (i,text) for i,text in enumerate(t['how'],1))
    out.extend(['','## '+t['directory_title'],'',
                '| '+' | '.join(t['headers'])+' |',
                '|---:|---|---|---:|---|---|---|---|'])
    for d in ds:
        idx=d['index']
        name=d.get('name_en') or d.get('name_zh') or d['id']
        fields=[f'{idx:02d}',f'[{md(name)}](docs/DATASET_DETAILS.md#dataset-{idx:02d})',
                disp(d['institution']),disp(d['year']),t['types'].get(d['resource_type'],d['resource_type']),
                tags_text(d),link(d['access_url'],t['access']),primary_paper(d,bypaper,True)]
        out.append('| '+' | '.join(fields)+' |')
    out.extend(['','## '+t['topic_title'],'',
                '| '+' | '.join(t['topic_headers'])+' |',
                '|---|---:|---|'])
    for key in tags_order:
        out.append('| [%s](docs/TOPICS.md#%s) | %s | %s |' % (key,key.lower(),tags[key],md(t['topics'][key])))
    out.extend(['','_'+t['topic_note']+'_','','## '+t['caveats_title'],''])
    out.extend('- '+x.format(**context) for x in t['caveats'])
    out.extend(['','## '+t['maintenance_title'],'',t['maintenance'],''])
    return '\n'.join(out)
