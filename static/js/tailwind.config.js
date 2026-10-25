    /* STRICT 3-COLOR DOMINANT SYSTEM:
       1. Cobalt Blue:      #1E3BFF
       2. Acid Lime Green:  #C6FF00
       3. Obsidian Black:   #141519
       (+ White/Surface untuk kontras ruang baca)
    */
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            hero: ['Unbounded', 'sans-serif'],
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            cobalt: '#1E3BFF',
            acid: '#C6FF00',
            obsidian: '#141519',
            surface: '#F4F5F8'
          }
        }
      }
    }
