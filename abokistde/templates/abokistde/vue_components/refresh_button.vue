<template id="refreshButton">
  <v-btn
      prepend-icon="mdi-refresh"
      @click="refreshVideos"
      :loading="loading"
  >Refresh
  </v-btn>
</template>

<script>
const refreshButton = {
  template: "#refreshButton",
  delimiters: ['[[', ']]'],
  inject: ["updateEpisodesCounter"],
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    refreshVideos() {
      this.loading = true
      axios({
        url: '/fetch_youtube'
      }).then(() => {
        this.updateEpisodesCounter++
        this.loading = false
      });
    }
  }
}
app.component("refreshButton", refreshButton)
</script>