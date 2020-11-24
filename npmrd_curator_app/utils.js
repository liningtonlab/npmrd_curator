export const POST_LOAD_JSCRIPT =
  'select all;set fontSize 14;label %a;select none;set picking select atom;'

export function minify( text ) {
  return text
    .split( '\n' )
    .map( ( x ) => x.trim() )
    .join( '' )
}

export function prettyJSON( json ) {
  if ( json ) {
    json = JSON.stringify( json, undefined, 4 )
    json = json.replace( /&/g, '&' ).replace( /</g, '<' ).replace( />/g, '>' )
    return json.replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function ( match ) {
        var cls = 'number'
        if ( /^"/.test( match ) ) {
          if ( /:$/.test( match ) ) {
            cls = 'key'
          } else {
            cls = 'string'
          }
        } else if ( /true|false/.test( match ) ) {
          cls = 'boolean'
        } else if ( /null/.test( match ) ) {
          cls = 'null'
        }
        return '<span class="' + cls + '">' + match + '</span>'
      }
    )
  }
}
