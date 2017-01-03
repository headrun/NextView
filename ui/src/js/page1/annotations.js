;(function($){
    "use strict";

    var _ = window._;//underscore js

    var _get_popover_tmpl;

    window.buzz_data = window.buzz_data || {};

    var keydown_whitelist = [38, 37, 40, 39];

    var blacklist_keys = [9, 13, 27, 220, 16, 17, 91, 218, 0, 38, 37, 40, 39, 45, 36, 33, 34, 35, 46, 12, 112, 113, 114, 115, 116, 117, 118];

    var setCaret = function(el, index) {


        if(!el) return;

        var range = document.createRange();
        var sel = window.getSelection();

        index = index || $(el)
            .text()
            .length;

        if (el.childNodes.length > 0) {

            range.setStart(el.childNodes[0], index);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        }
        $(el).focus().trigger("click");

        return el;
    }

    buzz_data.utils = {"show_message": function(msg) {window.alert(msg);}};

    // The Annotation constructor
    var Annotation = buzz_data.Annotation = function(graph_name, $graph, chart, point, data){

        graph_name = graph_name || "overview";

        var that = this;

        var new_annotation = !data;

        if(new_annotation){

            data = {"id": _.uniqueId("annotation-")};

            data["text"] = "";
            data["epoch"] = point.x;
            data["graph_name"] = graph_name;
            data["series_name"] = point.series.name;
        }

        if(graph_name == 'productivity_bar_graph'){

            var instance = chart.renderer.image('/img/marker.png',
                                                point.plotX + point.barX - 35,
                                                point.plotY - 15,
                                                20,
                                                24)
                                         .attr({
                                                "zIndex": 10,
                                                "class": "annotation-marker",
                                                "id": "annotation-" + data.id
                                              });
        }
        else {
               var instance = chart.renderer.image('/img/marker.png',
                                            point.plotX + chart.plotLeft - 10,
                                            point.plotY + chart.plotTop -30,
                                            20,
                                            24)
                                     .attr({
                                            "zIndex": 10,
                                            "class": "annotation-marker",
                                            "id": "annotation-" + data.id
                                          });

        }

        if($("body").hasClass("hide-annotations")){

            instance.attr({"style": "display:none"});
        }

        instance.add();

        this.$el = $(instance.element);
        this.xPos =  instance.x;
        this.yPos = instance.y;
        this.chart = chart;
        this.point = point;
        this.created = false;

        $("body").append(_get_popover_tmpl(data));

        this.$popover = $("#annotation-popover-" + data.id);

        var get_xpos = function(){

            //xpos is graph xpos  - half popover width - popover borderwidth + x offset
            return $graph.position().left + parseInt(that.$el.attr("x")) - that.$popover.width()/2 - 2 + 20;

        }

        var get_ypos = function(){

            // ypos is graph ypos - popover height - popover worderwith + y offset
            return $graph.position().top + parseInt(that.$el.attr("y")) - that.$popover.height() - 2 + 40;
        }

        var on_mouseenter = function(){

            show_annotation();
            setCaret(that.$popover.find("p").get(0));
        };

        var on_mouseleave = function(){

            that.$popover.find("p").blur();
            $(this).removeClass("in").removeClass("show");
        };

        var on_keydown = function(e){

            var yPos = get_ypos();
            that.$popover.css({"top": (yPos) + "px"});
            show_annotation();

            if($.inArray(e.which, keydown_whitelist) === -1 && $.inArray(e.which, blacklist_keys) >= 0){
                e.preventDefault();
                return false;
            }

        };

        var update_annotation = function(data){

            return $.post("/api/annotations/update/", data, function(){
            }, "json");
        };

        var on_keyup = function(e){

            if($.inArray(e.which, blacklist_keys) >= 0){
                return false;
            }

            var text = $(this).text();

            var $loading = that.$popover.find("i.annotation-loading").addClass("show");

            data.text = text;
            that.text = text;

            if(that.created){
               that.update(data, function(){

                    $loading.removeClass("show");
                });
            }

        };

        var delete_annotation = function(e){

            that.delete_annotation();
        };

        var show_annotation = function(){

            /*
            var other_series = _.without(that.chart.series, that.point.series);

            $.each(other_series, function(){

                this.hide();
            });
            */

            $("body > div.annotation-popover").filter(".show").removeClass("show");

            var xPos = get_xpos();
            var yPos = get_ypos();

            that.$popover.css({"top": (yPos) + "px", "left": (xPos) + "px"}).addClass("show").addClass("in");

            var $arrow = that.$popover.find("div.arrow").css({"left": "50%"});

            if(xPos < $graph.position().left){


                var diff = $graph.position().left - xPos + 10;

                that.$popover.css({"left": "+="+ diff});

                $arrow.css({"left": "-=" + diff});
            }

            if(xPos + that.$popover.width() > $(window).width()){
                var window_width = $(window).width();

                // 10 is offset
                var popover_position = xPos + that.$popover.width() + 10;

                var diff = popover_position - window_width;

                that.$popover.css({"left": "-="+ diff});

                $arrow.css({"left": "+=" + diff});

            }

            if($(this).parents("#project-sidebar").length > 0){

                setCaret($(this).find("p").get(0));
            }
        };

        if(new_annotation){
            show_annotation();
            setCaret(this.$popover.find("p").get(0));
        }

        var hide_annotation = function(){
            /*
            var other_series = _.without(that.chart.series, that.point.series);

            $.each(other_series, function(){

                this.show();
            });
            */
            that.$popover.removeClass("show");
        };

        var redraw = function(){

            that.redraw();
        };

        this.redraw = function(){

            var series_enabled = this.point.series.visible;

            if(!series_enabled){

                this.$el.fadeOut();
                this.$annotations_ul.fadeOut();
            }else{

                this.$el.attr({"y": this.point.plotY + this.chart.plotTop -30, "x": this.point.plotX + this.chart.plotLeft - 10});

                if(!$("body").hasClass("hide-annotations")){
                    this.$el.fadeIn();
                }

                this.$annotations_ul.fadeIn();
            }
        };

        var show_annotation_marker = function(){

            var series_enabled = that.point.series.visible;

            series_enabled ? that.$el.fadeIn(): that.$el.fadeOut();
        };

        var hide_annotation_marker = function(){

            that.$el.fadeOut();
        };

        this.bind_events = function(){

            this.$el.on("mouseenter", on_mouseenter);

            this.$popover.on("mouseleave", on_mouseleave)
                         .on("keydown", "div.popover-content > p", on_keydown)
                         .on("keyup", "div.popover-content > p", on_keyup)
                         .on("click", "span.glyphicon-trash", delete_annotation);

            $("body").on(data.graph_name + ".redraw", redraw)
                     .on("annotations.hide", hide_annotation_marker)
                     .on("annotations.show", show_annotation_marker);
        };

        this.bind_events();

        this.unbind_events = function(){

            this.$el.off("mouseenter", on_mouseenter);

            this.$popover.off("mouseleave", on_mouseleave)
                         .off("keydown", "div.popover-content > p", on_keydown)
                         .off("keyup", "div.popover-content > p", on_keyup)
                         .off("click", "span.glypglyphicon-trashh", delete_annotation);

            $("body").off(data.graph_name + ".redraw", redraw)
                     .off("annotations.hide", hide_annotation_marker)
                     .off("annotations.show", show_annotation_marker);
        }

        _.extend(this, data);

        var update_req = {};

        this.update = function(data, callback){

            if(update_req.abort){
                update_req.abort();
            }

            update_req = update_annotation(data);

            update_req.done(function(){

                update_req = {};
                callback();
            }).fail(function(){

                update_req = {};
                callback();
            });
            return this;
        };

        this.create_annotation = function(data, callback){

            return this.update();
        }

        this.destroy = function(){

            this.unbind_events();
            this.collection = _.without(this.collection, this);
            this.$el.remove();
        }

        var delete_annotaion = function(){

            return $.post("/api/annotations/update/", _.extend({"action": "delete"}, data), function(resp){

            });
        };

        var save_annotation = function(){

            return $.post("/api/annotations/update/", _.extend({"action": "update"}, data), function(resp){
                
            });
        };

        this.delete_annotation = function(callback) {

            this.destroy();

            var delete_annotation = delete_annotaion();

            var $loading = this.$popover.find("i.annotation-loading").addClass("show");

            delete_annotation.done(function(){

                $loading.removeClass("show");
                that.$popover.remove();
                that.$el.remove();

            }).fail(function(){

                buzz_data.utils.show_message("Unable to delete annotation");
                $loading.removeClass("show");
                that.bind_events();
            });

            return this;
        }

        if(new_annotation){

            this.$popover.find("i.annotation-loading").addClass("show");

            $.post("/api/annotations/create/", data, function(resp){

                resp = resp.result;

                var id = resp.id,
                    old_id = that.id;

                data.id  = id;

                that.$el.attr({"id": that.$el.attr("id").replace(old_id, id)});
                that.$popover.attr({"id": that.$popover.attr("id").replace(old_id, id)});

                that.created = true;

            }).fail(function(){

                buzz_data.utils.show_message("Unable to create annotation");
                that.delete_annotation();
            }).always(function(){

                that.$popover.find("i.annotation-loading").removeClass("show");
            });
        }else{

            this.created = true;
        }

        this.collection.push(this);

    };

    Annotation.prototype.collection = [];

    $(function () {

      _get_popover_tmpl = _.template($("#annotation-popover-tmpl").text());
    });
}(window.jQuery));
