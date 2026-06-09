(function ($) {
  /**
   * Esta função tem como finalidade pegar os valores digitados no formulário
   * e converter para uma string json
   */
  $.fn.serializeFormJSON = function (index) {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
      this.name = this.name.replace("__prefix__", index);
      if (o[this.name]) {
        if (!o[this.name].push) {
          o[this.name] = [o[this.name]];
        }
        o[this.name].push(this.value || "");
      } else {
        o[this.name] = this.value || "";
      }
    });
    return o;
  };
  /**
   * Está função fica responsável por gerar a tabela
   * do inline no localStorage
   */
  $.init = function initTable(obj) {
    obj.table = localStorage.getItem(obj.table_name); // Recupera os dados armazenados
    obj.table = JSON.parse(obj.table); // Converte string para objeto
    if (obj.table == null)
      // Caso não haja conteúdo, iniciamos um vetor vazio
      obj.table = [];
  };
  /**
   * Esta função tem como finalidade gerar a tabela do inline
   * recebe o objeto com as opções por parametro
   */
  $.getDataTable = function getDataTable(obj) {
    //remove a tabela antiga
    $("#table-" + obj.prefix + " tbody").html("");
    //remove o botão antigo
    $("#total-" + obj.prefix).html("");
    // Recuperar index do inline
    obj.index = obj.table.length;
    // Atualiza o campo TOTAL_FORMS
    $("input[name=" + obj.prefix + "-TOTAL_FORMS]").val(obj.index);
    var html = "";
    //Gera a tabela com os campos passados pelo usuário
    obj.table.forEach(function (item, i) {
      //se o item não esta deletado, mostra na tabela
      if(!(item[obj.prefix+"-"+i+"-DELETE"])){
      html += "<tr>";
      html +=
        '<td><button type="button" id="btn-edit-' +
        obj.prefix +
        '" data-id="' +
        i +
        '" \
                class="btn btn-link btn-sm data-toggle="tooltip" data-placement="right" title="Editar Registro."" >';
      html += '<i class="fa fa-edit"></i> </button>';
      html +=
        '<button type="button" id="btn-delete-' +
        obj.prefix +
        '" data-id="' +
        i +
        '" data-toggle="tooltip" data-placement="right" title="Excluir Registro." \
                class="btn btn-link text-muted btn-sm">';
      html += '<i class="fa fa-trash"></i> </button></td>';
      obj.fields.forEach(function (field) {
        var key = obj.prefix + "-" + i + "-" + field.toLowerCase();
        html += "<td>" + item[key] + "</td>";
      });
      html += "</tr>";
    }
    });
    // Inisere as linhas na tabela
    $("#table-" + obj.prefix + " tbody").append(html);
    // Adiciona o botão
    $("#total-" + obj.prefix).append(
      '<button type="button" class="btn btn-primary float-right" id="btn-add-' +
      obj.prefix +
      '">Adicionar Novo</button>'
    );
  };
  /**
   * Essa função e responsável por pegar os dados do formulário e inserir no LocaStorage
   * @param {*} obj: contém as opções do inline
   */
  $.create = function create(obj) {
    //Remove a máscara dos campos de data
    $("#form-" + obj.prefix+ ' .datefield').each(function () {
      $(this).val(
        $(this)
        .val()
        .split("/")
        .reverse()
        .join("-")
      );
    });
    // Pegar os dados do formulário e transforma em uma string JSON
    var data = $("#form-" + obj.prefix).find("select, textarea, input").serializeFormJSON(obj.index);
    // Insere os dados na tabela de opções do inline
    obj.table.push(data);
    // Insere a tabela com os novos dados no localStorage
    localStorage.setItem(obj.table_name, JSON.stringify(obj.table));
    //Gera um nova tabela
    $.getDataTable(obj);
    //Fecha o modal do formulário
    $("#form-" + obj.prefix + "-modal").modal("hide");
    //Mostra o alerta de successo
    $("#result-" + obj.prefix).append(
      '<div class="alert alert-success alert-dismissible fade show" role="alert">\
                <strong>Successo!</strong> Item criado com successo.\
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button></div>'
    );
    // Remove o alerta depois de um tempo
    $("#result-" + obj.prefix)
      .fadeTo(2000, 500)
      .slideUp(500, function () {
        $("#result-" + obj.prefix).slideUp(500);
        $("#result-" + obj.prefix).html("");
      });
  };
  /**
   * Esta função é responsável por atualizar uma linha da tabela
   * @param {*} event: evento do click do botão que ja vem com as opções do inline
   */
  $.update = function update(obj, id) {
    //Remove a máscara dos campos de data
    $("#form-" + obj.prefix+ ' .datefield').each(function () {
      $(this).val(
        $(this)
        .val()
        .split("/")
        .reverse()
        .join("-")
      );
    });
    // Pegar os dados do formulário transforma em JSON
    // depois substitui na tabela de opções
    obj.table[id] = $("#form-" + obj.prefix).find("select, textarea, input").serializeFormJSON(id);
    // Insere a tabela com os novos dados no localStorage
    localStorage.setItem(obj.table_name, JSON.stringify(obj.table));
    // Gera uma nova tabela no html
    $.getDataTable(obj);
    $("#form-" + obj.prefix + "-modal").modal("hide");
    //Mostra o alerta de successo
    $("#result-" + obj.prefix).append(
      '<div class="alert alert-success alert-dismissible fade show" role="alert">\
            <strong>Successo!</strong> Item editado com successo.\
            <button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button></div>'
    );
    //Coloca um tempo no alerta
    $("#result-" + obj.prefix)
      .fadeTo(2000, 500)
      .slideUp(500, function () {
        $("#result-" + obj.prefix).slideUp(500);
        $("#result-" + obj.prefix).html("");
      });
  };
  /**
   * Esta função é responsável por remover uma linha da tabela
   * @param {*} event: evento do click do botão que ja vem com as opções do inline
   */
  $.delete = function remove(event) {
    event.preventDefault();
    // Recuperar as opções do inline que vem no evento
    var obj = event.data.obj;
    // Recupera o id da linha da tabela
    var id = event.data.id;
    // atualiza o objeto para deletar no servidor
    obj.table[id][obj.prefix+"-"+id+"-DELETE"] = true;
    // Atualiza o localStorage
    localStorage.setItem(obj.table_name, JSON.stringify(obj.table));
    // Gera uma nova tabela
    $.getDataTable(obj);
    // Fecha o modal de delete
    $("#form-delete-" + obj.prefix + "-modal").modal("hide");
    //Mostra o alerta de successo
    $("#result-" + obj.prefix).append(
      '<div class="alert alert-success alert-dismissible fade show" role="alert">\
                        <strong>Successo!</strong> Item deletado com successo.\
            <button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button></div>'
    );
    // Tira o alert com base no tempo
    $("#result-" + obj.prefix)
      .fadeTo(2000, 500)
      .slideUp(500, function () {
        $("#result-" + obj.prefix).slideUp(500);
        $("#result-" + obj.prefix).html("");
      });
  };
  /**
   * Esta função é responsável por pegar os dados do localstorage
   * e passar par ao modal para o usuário atualizar os dados
   * @param {*} id: id da linha no modal
   * @param {*} obj: objeto com as opções do inline
   */
  $.passDataModal = function passDataModal(id, obj) {
    //pega o item com base no Id
    var item = obj.table[id];
    // Pega os inputs do formulário
    var inputs = $("#form-" + obj.prefix + " :input");
    // pega o index o objeto item
    var sortedKeys = Object.keys(item)[0].split('-')[1];
    // para cada input coloca o valor do localstorage
    inputs.each(function () {
      //Pega o nome do campo e substitui o prefix pelo index
      // para depois adiconar o valor correspondente ao campo
      var name = $(this).attr("name").replace("__prefix__", sortedKeys);
      $(this).val(item[name].split("-").reverse().join("/"));
    });
  };
  /**
   * Função responsável por pegar todos os dados inseridos no localstorage
   */
  $.getAll = function allStorage() {
    var values = [],
      keys = Object.keys(localStorage),
      i = keys.length;
    while (i--) {
      if(keys[0].substring(0, 6) == 'inline'){
        values.push(localStorage.getItem(keys[i]));
      }
    }
    return values;
  };
  /**
   * Função responsável para verificar o max de forms que o formset permite
   * @param {*} obj : objeto com as opções do inline
   */
  $.hasMaxForms = function (obj) {
    var maxForms =
      parseInt($("input[name=" + obj.prefix + "-MAX_NUM_FORMS]").val(), 10) ||
      1000;
    return maxForms;
  };
  /**
   * Função responsável para verificar o min de forms que o formset permite
   * @param {*} obj : objeto com as opções do inline
   */
  $.hasMinForms = function (obj) {
    var minForms =
      parseInt($("input[name=" + obj.prefix + "-MIN_NUM_FORMS]").val(), 10) ||
      0;
    return minForms;
  };
  /**
   * Função responsável por validar o formulário com base na API
   * @param {*} event
   */
  $.validateForm = function (event) {
    event.preventDefault();
    var obj = event.data.obj;
    // Remove a máscara dos campos de data para que seja enviado no formato
    //de salvar no banco de dados.
    if ($("#form-" + obj.prefix + " input").hasClass("datefield")) {
      $(".datefield").val(
        $(".datefield")
        .val()
        .split("/")
        .reverse()
        .join("-")
      );
    }
    // Recuperar o  csrf token  do formulário
    // Se não for inserido a API retorna um error 403
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    // Pega os dados digitados no formulário
    var data = $("#form-" + obj.prefix)
      .find("select, textarea, input")
      .serialize();
    // Expressão regular para remover o prefix do formset
    // Para deixar os campos iguais ao do model
    var find = obj.prefix + "-__prefix__-";
    var re = new RegExp(find, "g");
    data = data.replace(re, "");
    // Insere o csrftoken no dados passados pelo ajax
    data = data + "&csrfmiddlewaretoken=" + csrftoken;
    // Ajax que valida o formulário
    $.ajax({
      url: "/core/api/" + obj.app + "/" + obj.prefix + "/validate/",
      method: "POST",
      data: data,
      dataType: "json",
      success: function (data) {
        //Remove os errors dos formulário
        $("#form-" + obj.prefix + " input, select")
          .removeClass("is-invalid")
          .next(".invalid-feedback")
          .remove();
          typeof event.data.id === 'undefined' ? $.create(obj) : $.update(obj, event.data.id);
      },
      error: function (error) {
        //Remove os errors antigos
        $("#form-" + obj.prefix + " input, select")
          .removeClass("is-invalid")
          .next(".invalid-feedback")
          .remove();
        //Pega as mensagens de erro e tranformar em um json
        console.log(error.responseText);
        // TODO: Corrigir esse parse abaixo.
        var errors = JSON.parse(error.responseText);
        //pra cada erro adiciona a mensagem abaixo do campo
        $.each(errors, function (i, v) {
          var msg = '<div class="invalid-feedback">' + v + "</div>";
          $(
              "#form-" +
              obj.prefix +
              ' input[name="' +
              obj.prefix +
              "-__prefix__-" +
              i +
              '"], select[name="' +
              obj.prefix +
              "-__prefix__-" +
              i +
              '"]'
            )
            .addClass("is-invalid")
            .after(msg);
        });
        //Foca na primeiro campo de erro
        var keys = Object.keys(errors);
        $(
          "#form-" +
          obj.prefix +
          ' input[name="' +
          obj.prefix +
          "-__prefix__-" +
          keys[0] +
          '"]'
        ).focus();
        //Se o campo que deu erro e hidden, cria o objeto
        // Quando os dados são mandando os form não valida por que não tem o foreign key do pai
        // precisa desse if para verificar se o erro e da foreign key do pai
        // se for pode criar o objeto, porque a foreign key vai ser criada depois
        if ($("#form-" + obj.prefix + ' input[name="' + obj.prefix + "-__prefix__-" + keys[0] + '"]').attr('type') == 'hidden') {
          typeof event.data.id === 'undefined' ? $.create(obj) : $.update(obj, event.data.id);
        }
      }
    });
  };
})(jQuery);