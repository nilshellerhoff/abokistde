<template id="templateLoadingIndicator">
  <img src="/static/assets/logo_animated.svg" style="height: 100%; width: 100%; display: block;"/>
</template>

<script>
const loadingIndicator = {
  template: '#templateLoadingIndicator',
  delimiters: ['[[', ']]'],
}
app.component('loadingIndicator', loadingIndicator)
</script>