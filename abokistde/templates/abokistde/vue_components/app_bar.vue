<template id="templateAppBar">
  <v-app-bar
      color="primary"
      prominent
  >
    <v-app-bar-nav-icon variant="text"
                        @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

    <v-toolbar-title>[[ title ]]</v-toolbar-title>
    <v-spacer></v-spacer>
<!--    <dark-theme-toggle></dark-theme-toggle>-->

    <v-btn href="/accounts/logout" prepend-icon="mdi-logout">Logout</v-btn>

  </v-app-bar>
  <channel-list></channel-list>
</template>

<script>
const appBar = {
  template: '#templateAppBar',
  delimiters: ['[[', ']]'],
  props: ['title'],
  inject: ['drawer'],
  data() {
    return {
      channels: window.channels,
    }
  },
  computed: {}
}

app.component('appBar', appBar);
</script>