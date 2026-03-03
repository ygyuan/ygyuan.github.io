# Publications markdown generator for ygyuan
#
# Takes a TSV / CSV of publications with metadata and converts them for use with [ygyuan.github.io](ygyuan.github.io). 
# Can be called via the command prompt by using `python3 publications.py [filename]`.
#
# Data format
# 
# The file needs to have the following columns as a header at the top:
# pub_date, title, venue, excerpt, citation, url_slug, paper_url, slides_url
# - `excerpt`, `paper_url`, and slides_url can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. 
#    The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`
import csv
import os
import sys
import re
import html

# Flag to indicate an error occurred
EXIT_ERROR = 0

# The expected layout of the CSV / TSV file
HEADER_LEGACY  = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url']
HEADER_UPDATED = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url', 'category']

# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands)
# with their HTML encoded equivalents. This makes them look not so readable in raw format, but they are parsed and
# rendered nicely.
HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(HTML_ESCAPE_TABLE.get(c,c) for c in text)

def parse_bibtex_file(filename: str):
    """Parse a BibTeX file using regex and return a list of entries."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'%.*?\n', '\n', content)
        
        # Find all @ entries using a more robust pattern
        entries = []
        # Split content by @ entries
        entry_pattern = r'@(\w+)\s*\{\s*([^,]+),\s*([^@]+?)(?=@|$)'
        matches = re.findall(entry_pattern, content, re.DOTALL)
        
        for match in matches:
            entry_type, entry_key, fields_str = match
            
            # Parse fields
            fields = {}
            # Handle both { } and " " formats, and nested braces
            field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|(\w+)\s*=\s*"([^"]*)"'
            field_matches = re.findall(field_pattern, fields_str)
            
            for field_match in field_matches:
                if field_match[0]:  # { } format
                    field_name = field_match[0]
                    field_value = field_match[1]
                else:  # " " format
                    field_name = field_match[2]
                    field_value = field_match[3]
                
                # Clean up field value
                field_value = re.sub(r'\\n', ' ', field_value)
                field_value = re.sub(r'\\"', '"', field_value)
                field_value = re.sub(r'\\&', '&', field_value)
                field_value = field_value.strip()
                fields[field_name.lower()] = field_value
            
            entries.append({
                'type': entry_type,
                'key': entry_key,
                'fields': fields
            })
        
        return entries
    except Exception as e:
        print(f'ERROR parsing BibTeX file: {e}', file=sys.stderr)
        sys.exit(EXIT_ERROR)

def process_bibtex_file(filename: str):
    """Process a BibTeX file and convert to markdown files."""
    entries = parse_bibtex_file(filename)
    
    for entry in entries:
        try:
            b = entry['fields']
            
            # Parse date
            pub_year = b.get('year', '1900')
            pub_month = b.get('month', '01')
            pub_day = b.get('day', '01')
            
            # Handle month formatting
            if len(pub_month) < 3:
                pub_month = "0" + pub_month
                pub_month = pub_month[-2:]
            else:
                month_mapping = {
                    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                }
                month_lower = pub_month.lower()[:3]
                if month_lower in month_mapping:
                    pub_month = month_mapping[month_lower]
            
            pub_date = f"{pub_year}-{pub_month}-{pub_day}"
            
            # Clean title for URL slug
            clean_title = b.get('title', '').replace("{", "").replace("}", "").replace("\\", "")
            url_slug = re.sub(r'[^a-zA-Z0-9_-]', "", clean_title.replace(" ", "-"))
            url_slug = url_slug.replace("--", "-")
            
            md_filename = f"{pub_date}-{url_slug}.md"
            html_filename = f"{pub_date}-{url_slug}"
            
            # Build citation
            citation = ""
            
            # Authors - handle LaTeX formatting more robustly
            authors = b.get('author', '')
            if authors:
                # Clean LaTeX formatting
                authors = re.sub(r'\\textbf\{([^}]*)\}', r'\1', authors)  # Remove \textbf{}
                authors = re.sub(r'\\textf\{([^}]*)\}', r'\1', authors)  # Remove \textf{}
                authors = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', authors)  # Remove other LaTeX commands
                authors = authors.replace("{", "").replace("}", "")  # Remove remaining braces
                
                author_list = authors.split(' and ')
                for author in author_list:
                    # Simple author name extraction
                    parts = author.strip().split(',')
                    if len(parts) > 1:
                        last_name = parts[0].strip()
                        first_name = parts[1].strip() if len(parts) > 1 else ""
                        citation += f"{first_name} {last_name}, "
                    else:
                        citation += f"{author.strip()}, "
            
            # Title
            title = b.get('title', '').replace("{", "").replace("}", "").replace("\\", "")
            citation += f'"{html_escape(title)}."'
            
            # Venue
            venue = b.get('journal', b.get('booktitle', b.get('venue', '')))
            citation += f" {html_escape(venue)}, {pub_year}."
            
            # YAML metadata
            md = f"---\ntitle: \"{html_escape(title)}\"\n"
            md += "collection: publications\n"
            md += f"permalink: /publication/{html_filename}\n"
            
            # Excerpt/note
            note = b.get('note', '')
            if len(note) > 5:
                md += f"excerpt: '{html_escape(note)}'\n"
            
            md += f"date: {pub_date}\n"
            md += f"venue: '{html_escape(venue)}'\n"
            
            # Paper URL
            paper_url = b.get('url', b.get('paperurl', ''))
            if len(paper_url) > 5:
                md += f"paperurl: '{paper_url}'\n"
            
            md += f"citation: '{html_escape(citation)}'\n"
            
            # Category based on entry type
            if entry['type'] == 'article':
                md += "category: manuscripts\n"
            else:
                md += "category: conferences\n"
            
            md += "---\n"
            
            # Markdown content
            if len(note) > 5:
                md += f"\n{html_escape(note)}\n"
            
            if len(paper_url) > 5:
                md += f"\n[Access paper here]({paper_url}){{:target=\"_blank\"}}\n"
            else:
                md += f"\nUse [Google Scholar](https://scholar.google.com/scholar?q={html.escape(clean_title.replace('-', '+'))}){{:target=\"_blank\"}} for full citation"
            
            # Write the file
            md_filename = os.path.join("../_publications/", os.path.basename(md_filename))
            with open(md_filename, 'w', encoding="utf-8") as f:
                f.write(md)
            
            print(f'SUCCESSFULLY PARSED {entry["key"]}: \"{title[:60]}{"..." if len(title) > 60 else ""}\"')
            
        except Exception as e:
            print(f'WARNING Error processing entry {entry.get("key", "unknown")}: {e}')
            continue

# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to
# concatenate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then
# does the description for the individual page.
def create_md(lines: list, layout: list):
    for item in lines:
        # Parse the filename information
        md_filename = f"{item[layout.index('pub_date')]}-{item[layout.index('url_slug')]}.md"
        html_filename = str(item[layout.index('pub_date')]) + "-" + item[layout.index('url_slug')]
        
        # Parse the YAML variables
        md = f"---\ntitle: \"{item[layout.index('title')]}\"\n"
        md += "collection: publications"
        if len(layout) == len(HEADER_UPDATED):
            md += f"\ncategory: {item[layout.index('category')]}"
        else:
            md += "\ncategory: manuscripts"
        md += f"\npermalink: /publication/{html_filename}"
        if len(str(item[layout.index('excerpt')])) > 5:
            md += f"\nexcerpt: '{html_escape(item[layout.index('excerpt')])}'"
        md += f"\ndate: {item[layout.index('pub_date')]}"
        md += f"\nvenue: '{html_escape(item[layout.index('venue')])}'"
        if len(str(item[layout.index('paper_url')])) > 5:
            md += f"\npaperurl: '{item[layout.index('paper_url')]}'"
        md += f"\ncitation: '{html_escape(item[layout.index('citation')])}'"
        md += "\n---"
        
        # Markdown description for individual page
        if len(str(item[layout.index('paper_url')])) > 5:
            md += f"\n<a href='{item[layout.index('paper_url')]}'>Download paper here</a>\n"
        if len(str(item[layout.index('excerpt')])) > 5:
            md += f"\n{html_escape(item[layout.index('excerpt')])}\n"
        md += f"\nRecommended citation: {item[layout.index('citation')]}"
        
        # Write the file
        md_filename = os.path.join("../_publications/", os.path.basename(md_filename))
        with open(md_filename, 'w') as f:
            f.write(md)

def read(filename: str) -> tuple[list, list]:
    '''Read the contents of the file, check the header and return the parsed line along with the file type.'''

    # Read the contents of the file
    lines = []
    with open(filename, 'r') as file:
        delimiter = ',' if filename.endswith('.csv') else '\t'
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            lines.append(row)

    # Verify the file format makes sense
    if len(lines) <= 1:
        print(f'Not enough lines in the file to process, found {len(lines)}', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # Verify the header, remove it once checked
    layout = HEADER_UPDATED
    if HEADER_LEGACY == lines[0]:
        layout = HEADER_LEGACY
    elif HEADER_UPDATED != lines[0]:
        print(lines[0])
        print('The header of the file does not match the expected format', file=sys.stderr)
        sys.exit(EXIT_ERROR)
    lines = lines[1:]
    
    # Return the lines and format
    return lines, layout

if __name__ == '__main__':
    # Make sure a filename was given
    if len(sys.argv) != 2:
        print('Usage: python3 publications.py [filename]', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # Get the filename
    filename = sys.argv[1]
    
    # Check file type and process accordingly
    if filename.endswith('.bib'):
        print(f'Processing BibTeX file: {filename}')
        process_bibtex_file(filename)
    elif filename.endswith('.csv') or filename.endswith('.tsv'):
        print(f'Processing CSV/TSV file: {filename}')
        lines, layout = read(filename)
        create_md(lines, layout)
    else:
        print(f'Expected a BibTeX, TSV or CSV file, got {filename}', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    print('Processing completed successfully!')
