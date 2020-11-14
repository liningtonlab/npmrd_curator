export function minify(text) {
  return text
    .split('\n')
    .map((x) => x.trim())
    .join('')
}
