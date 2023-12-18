<template id="templateRemoveChannelButton">
  <v-btn
      icon="mdi-minus"
      @click="removeChannel"
      @click.prevent=""
  ></v-btn>
</template>

<script>
const removeChannelButton = {
  template: '#templateRemoveChannelButton',
  props: ['channel'],
  data() {
    return {}
  },
  methods: {
    removeChannel: async function (result) {
      if (confirm(`Remove ${this.channel.name} from subscriptions?`)) {
        axios({
          method: 'post',
          url: '/api/delete_channel',
          data: {
            channelid: this.channel.id
          }
        }).then(() => {
          location.reload()
        });
      }
    }

  }
}
app.component("removeChannelButton", removeChannelButton)
</script>