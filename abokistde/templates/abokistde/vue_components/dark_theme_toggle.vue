<template id="templateDarkThemeToggle">
  <v-btn
      @click="switchMode"
  >dark mode</v-btn>
</template>

<script>
const darkThemeToggle = {
  template: "#templateDarkThemeToggle",
  methods: {
    switchMode() {
      console.log(this.$vuetify)
      console.log(this.$vuetify.theme)
      console.log(this.$vuetify.theme.dark)
      // this.$vuetify.theme.dark = !this.$vuetify.theme.dark
    }
  }
}
app.component("darkThemeToggle", darkThemeToggle)
</script>