// require.config({
//     shim: {
//         'input-mask': ['jquery', 'core']
//     },
//     paths: {
//         'input-mask': 'assets/plugins/input-mask/js/jquery.mask.min'
//     }
// });

$( document ).ready(function() {
   $('input[input-mask="money"]').mask("#.##0,00", {reverse: true});
});

