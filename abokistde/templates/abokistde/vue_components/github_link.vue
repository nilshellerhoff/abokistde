<template id="templateGithubLink">
        <div class="pa-2">
        <v-btn
            block
            variant="outlined"
            color="primary"
            href="https://github.com/nilshellerhoff/abokistde"
            target="_blank"
        >
          <img src="https://github.githubassets.com/favicons/favicon.png"
               style="height: 20px; margin-right: 4px">Github
        </v-btn>
      </div>

</template>
<script>
const githubLink = {
  template: '#templateGithubLink'
}
app.component("githubLink", githubLink)
</script>