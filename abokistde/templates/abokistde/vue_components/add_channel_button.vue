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
  props: ['channelId'],
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    addChannel: async function (result) {
      this.loading = true;
      axios({
        method: 'post',
        url: '/api/insert_channel_by_id',
        data: {
          channel_id: this.channelId,
        }
      }).then(() => {
        // this.loading = false
        location.reload()
      }).catch(() => {
        // this.loading = false;
      })
    }

  }
}

app.component("addChannelButton", addChannelButton)

</script>