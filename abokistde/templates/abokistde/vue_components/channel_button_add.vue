<template id="templateAddChannelButton">
  <v-btn
      icon="mdi-plus"
      @click="addChannel"
      :loading="loading"
  ></v-btn>
</template>

<script>
const addChannelButton = {
  template: '#templateAddChannelButton',
  inject: ["updateEpisodesCounter", "updateChannelsCounter"],
  props: ['channel'],
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    addChannel() {
      this.loading = true;
      axios({
        method: 'post',
        url: '/api/user_subscription/',
        data: {
          publishing_channel_id: this.channel.id,
        },
        headers: {"X-CSRFToken": window.csrftoken},
      }).then(() => {
        this.updateEpisodesCounter++
        this.updateChannelsCounter++
      }).finally(() => {
        this.loading = false;
      })
    }
  }
}
app.component("addChannelButton", addChannelButton)
</script>