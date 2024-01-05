<template id="templateAppBar">
  <v-app-bar
      color="primary"
      prominent
  >
    <v-app-bar-nav-icon variant="text"
                        @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <img class="ml-2 py-4" style="height: 100%" src="/static/assets/logo.svg">
    <v-toolbar-title>[[ title ]]</v-toolbar-title>
    <v-spacer></v-spacer>
<!--    <dark-theme-toggle></dark-theme-toggle>-->

    <v-btn href="/accounts/logout/" icon="mdi-logout"></v-btn>

  </v-app-bar>
  <channel-list></channel-list>
</template>

<script>
const appBar = {
  template: '#templateAppBar',
  delimiters: ['[[', ']]'],
  props: ['title'],
  inject: ['drawer'],
}

app.component('appBar', appBar);
</script>