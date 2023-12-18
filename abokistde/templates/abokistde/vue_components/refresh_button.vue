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
        location.reload()
      });
    }
  }
}
app.component("refreshButton", refreshButton)
</script>