<template id="templateChannelFilterButton">
  <div style="height: 40px">
  <span v-if="channelFilter">
    <v-btn variant="text"
           append-icon="mdi-window-close"
           @click="channelFilter = null"
           height="50px"
           style="text-transform: unset !important;"
    >
      <template #prepend>
        <v-avatar :image="channelFilter.thumbnail_url"></v-avatar>
      </template>
      [[ channelFilter.name ]]
    </v-btn>
  </span>
  </div>
</template>

<script>
const channelFilterButton = {
  delimiters: ['[[', ']]'],
  inject: ["channelFilter"],
  template: '#templateChannelFilterButton',
}
app.component('channelFilterButton', channelFilterButton)
</script>