<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Markdown</div>
      <div class="card-body">
        <VueShowdown
          flavor="github"
            markdown='
# Showdown

Showdown is a Javascript Markdown to HTML converter, based on the original works by John Gruber.
Showdown can be used client side (in the browser) or server side (with NodeJs).

## Live DEMO

Check a live Demo here http://demo.showdownjs.com/

## [![Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=11141581)

As you know, ShowdownJS is a free library and it will remain free forever. However, maintaining and improving the library costs time and money.

If you like our work and find our library useful, please donate through [patreon](https://www.patreon.com/showdownjs) or directly through [paypal](https://www.paypal.me/tiviesantos)!! Your contribution will be greatly appreciated and help me continue to develop this awesome library.

## License

ShowdownJS v 2.0 is release under the MIT version. Previous versions are release under BSD.
  '/>
      </div>
    </div>
  </div>
</template>

<script>
</script>

<style>
</style>
