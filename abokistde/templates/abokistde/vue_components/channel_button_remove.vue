<template id="templateRemoveChannelButton">
  <v-btn
      icon="mdi-minus"
      @click.stop="removeChannel"
  ></v-btn>
</template>

<script>
const removeChannelButton = {
  template: '#templateRemoveChannelButton',
  props: ['subscription'],
  inject: ["updateEpisodesCounter", "updateChannelsCounter"],
  data() {
    return {}
  },
  methods: {
    removeChannel() {
      if (confirm(`Remove ${this.subscription.publishing_channel.name} from subscriptions?`)) {
        this.loading = true;
        axios({
          method: 'delete',
          url: `/api/user_subscription/${this.subscription.id}/`,
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
}
app.component("removeChannelButton", removeChannelButton)
</script>