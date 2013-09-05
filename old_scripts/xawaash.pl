#!/usr/bin/perl
use strict;
use Net::Google::Spreadsheets;

#http://www.livejournal.com/doc/server/lj.install.perl_setup.modules.html

my @languages = ('english', 'somali', 'french', 'arabic');
my ($dictionary, %ingredients, %images, %html);
my $printNum = 0;
$html{arabic}{RightToLeft} = 1;
$html{arabic}{noUpper} = 1;
$html{french}{noUpper} = 1;

# allow special characters such as french accents and arabic characaters
binmode(STDOUT, ":utf8");

#set general style for arabic tables
my $arabic_table_style = "float:right; margin-bottom: 3em; margin-left: 15em; text-align: right;";
my $arabic_text_style = "margin-left: 10em; float:right; text-align: right;";

sub lookup {
	my ($text, $column) = @_;
	print "$text, $column\n";
	my $search = "english = \"$text\"";
	my @rows = $dictionary->rows({sq => $search});
	my $content = $rows[0]->content;
	print "$text, $column -> " . $content->{$column} . "\n" if $content->{$column};
	return $content->{$column};
}

sub listItem {
	my ($item, $language) = @_;
	if($language eq 'arabic'){
		return "<td style=\"padding: 0em 1em;\">$item</td>\n";
	} else {
		return "<li style=\"margin-bottom:0em;\">$item</li>\n";
	}
}

sub htmlIngredients {
	my $sheet = shift;
	my @rows = $sheet->rows();
	foreach my $language (@languages){
		$html{$language}{Ingredients} = $language eq 'arabic' ? "<table style=\"$arabic_table_style border-color:#c0c0c0;\" border=\"1\">\n" : "<ul>\n";
		my $firstsubheading = 1;
		foreach my $row (@rows) {
			my $content = $row->content;

			my $output;
			if ($language eq 'arabic'){

				#If the item is a subheading, create a merged cell spanning the width of the table
				if($content->{subheading}){
					my $text = lookup($content->{subheading}, $language);
					$html{$language}{Ingredients} .= "<tr>\n<td colspan=\"3\" style=\"font-weight:bold; padding-top:1em;\">" . $text . "</td>\n</tr>\n";
					next;
				}
		
				my $code = "<tr>\n";
				my $style = lookup($content->{style}, $language) if $content->{style};
				my $ingredient = lookup($content->{ingredient}, $language);
				$ingredient = "($ingredient( $style" if $style;
				my $link = lookup($content->{ingredient}, 'link');
				my $tag = "";
				$tag .= "href=\"" . $link . "\" " if $link;
				my $img = lookup($content->{ingredient}, 'image');
				if ($img) {
					my ($width, $height) = split(";", lookup($content->{ingredient}, 'imagestyle'));
					$tag .= "onmouseover=\"Tip('$ingredient &lt;br&gt;&lt;img src=$img width=$width height=$height &gt;', WIDTH, $width, PADDING, 6, BGCOLOR, '#ffffff')\" onmouseout=\"UnTip()\"";
				}
				$ingredient = $tag eq "" ? $ingredient : "<a title=\"$ingredient\" $tag target=\"_blank\">$ingredient</a>\n";
				$code .= listItem($ingredient, $language);

				if ($content->{unit} eq 'g') {
					$code .= listItem(lookup('g', $language), $language);
					$code .= listItem($content->{international}, $language);
				} else {
					my $measure = lookup($content->{measure}, $language) if $content->{measure};
					$code .= listItem($measure, $language);
					$code .= listItem($content->{quantity}, $language);
				}
				$html{$language}{Ingredients} .= "$code</tr>\n";
			#	if ($content->{size}){
			#	push @txt, "(Optional)" if $content->{optional} eq 'Yes';
			#	if ($content->{$language . "comment"}) {
			} else {

				#If the item is a subheading, end previous list and start a new one under new subheading
				if($content->{subheading}){
					my $text = lookup($content->{subheading}, $language);
					$html{$language}{Ingredients} .= "</ul>\n<span style=\"font-weight:bold;\">" . $text . ":</span>\n\n<ul style=\"margin:0;\">\n";
					next;
				}

				my @txt;
				my $quantity = $content->{quantity};
				#$quantity = $quantity =~ /(\d*)?\s?(\d*)\/(\d*)/ ? "$1&frac$2$3;" : $quantity;
				push @txt, $quantity;
				if ($content->{measure}) {
					my $measure = lookup($content->{measure}, $language);
					push @txt, $measure;
				}
				if ($content->{international}) {
					my $value = $content->{international};
					my $unit = $content->{unit};
					my $IU = $html{$language}{RightToLeft} ? "($unit $value)" : "($value $unit)";
					push @txt, $IU;
				}
				my $ingredient = lookup($content->{ingredient}, $language);
				$ingredient = ucfirst $ingredient unless $html{$language}{noUpper};
				push @txt, $ingredient;
				if ($content->{size}){
					my $size = lookup($content->{size}, $language);
					$size = ucfirst $size unless $html{$language}{noUpper};
					$size .= "oo " if $language eq 'Somali';
					push @txt, ", $size" if $size;
				}
				push @txt, "(" . lookup($content->{style}, $language) . ")" if $content->{style};
				push @txt, "(Optional)" if $content->{optional} eq 'Yes';
				if ($content->{$language . "comment"}) {
					push @txt, "-";
					my $comment = $content->{$language . "comment"};
					$comment = ucfirst $comment unless $html{$language}{noUpper};
					push @txt, $comment;
				}
				my $text = $html{$language}{RightToLeft} ? join(" ", reverse(@txt)) : join(" ", @txt);
	
				my $output = "";
	
				#link the text if there is a Link defined
				my $link = lookup($content->{ingredient}, 'link');
				$output .= "href=\"" . $link . "\" " if $link;
	
				#add a hover tooltip with image if there is one
				my $img = lookup($content->{ingredient}, 'image');
				if ($img) {
					my ($width, $height) = split(";", lookup($content->{ingredient}, 'imagestyle'));
					$output .= "onmouseover=\"Tip('$text &lt;br&gt;&lt;img src=$img width=$width height=$height &gt;', WIDTH, $width, PADDING, 6, BGCOLOR, '#ffffff')\" onmouseout=\"UnTip()\"";
				}
				#if there wasn't a tooltip or link defined, just output text
				$html{$language}{Ingredients} .= $output eq "" ? listItem($text, $language) : listItem("<a title=\"$text\" $output target=\"_blank\">$text</a>", $language);
			}
		}
		$html{$language}{Ingredients} .= $language eq 'arabic' ? "</table>\n\n" : "</ul>\n\n";
	}
}

sub htmlContent {
	my $sheet = shift;
	my %unique;
	
	# add the google translate button at the start of the page
	$html{scripts}{Content} = "<div id=\"google_translate_element\"></div>\n<script type=\"text/javascript\">// <![CDATA[\nfunction googleTranslateElementInit() {   new google.translate.TranslateElement({     pageLanguage: 'en'   }, 'google_translate_element'); }\n// ]]></script><script type=\"text/javascript\" src=\"//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit\"></script>\n\n";

	# add nbsps at the end of the post and a back to top link
	my $ind = 5;
	$html{footer}{Content} = "\n";
	while(0 < $ind--){
		$html{footer}{Content} .= "&nbsp;\n\n";
	}

	my @rows = $sheet->rows();
	foreach my $language (@languages){
		$html{$language}{Content} = "<div id=\"tabs-$language\"><br>\n";
		my ($lastImg, $lastCaption, $previous);
		my $direction_num = 1;
		foreach my $row (@rows){
			my $content = $row->content;
			my $section = $content->{section};
			if ($previous ne $section){
				if($previous eq 'Directions'){
					$direction_num = 1;
					my $close_tag = $language eq 'arabic' ? "</table>\n" : "</ol>\n";
					$html{$language}{Content} .= "$close_tag</div>\n\n";
				} elsif ($section eq 'Directions'){
					my $printNum = $html{$language}{printNum};
					my $style;
					$style = $arabic_text_style;
					my $open_tag = "<div id=\"$language$printNum\" style=\"display:none;\"><p style=\"$style\">$lastImg</p></div>";
					$images{"content$printNum"} = 1;
					$printNum++;
					$open_tag .= "<div id=\"$language$printNum\" style=\"display:none;\"><p style=\"$style\"><em>$lastCaption</em><p></div>";
					$printNum++;
					$open_tag .= "<div id=\"$language$printNum\">\n"; 
					$open_tag .= $language eq 'arabic' ? "<table style=\"$arabic_table_style\">\n" : "<ol>\n";
					$printNum++;
					$html{$language}{Content} .= $open_tag;
					$html{$language}{printNum} = $printNum;
				}
			}
			$previous = $section;

			#generate html for content;
			my $text = $content->{$language};
			my $code;
			my $printNum = $html{$language}{printNum} || 0;
			next unless $text || $section eq 'Ingredients';
			if ($section eq 'Introduction'){
				my $style = $content->{properties};
				$code = $style ? "<p style=\"$style\">$text</p>\n" : "<p>$text</p>\n";
			} elsif ($section eq 'Complete') {
				$html{$language}{complete} = $text eq 'Yes' ? 1 : 0;
				$text eq 'Yes' ? next : last;
			} elsif ($section eq 'Tab Name' && $html{$language}{complete}) {
				$html{tabs}{Content} .= "<li><a href=\"#tabs-$language\">$text</a></li>\n";
				next;
			} elsif ($section eq 'Header') {
				my $style = "font-size: medium; text-decoration: underline;";
				$style .= "text-align:right; margin-left:10em" if $language eq 'arabic';
				$code = "\n<div id=\"$language$printNum\"><p style=\"$style\"><strong>$text</strong></p></div>\n";
				$html{$language}{printNum}++;
			} elsif ($section eq 'Video') {
				my ($width, $height) = split(";", $content->{properties});
				$code = "<p style=\"text-align: center;\"><iframe src=\"$text\" frameborder=\"0\" width=\"$width\" height=\"$height\"></iframe></p>\n";
			} elsif ($section eq 'Printing') {
				my $style = "text-align:right;" if $language eq 'arabic';
				my $val = $content->{properties};
				$code = "<p style=\"$style\"><a onclick=\"printSelection('$language',$val);return false\">$text</a></p>\n";
			} elsif ($section eq 'Ingredients') {
				$code = $html{$language}{Ingredients};
				$code = "<div id=\"$language$printNum\">\n$code</div>";
				$html{$language}{printNum}++;
			} elsif ($section eq 'Directions') {
				$code = listItem($text, $language);
				$code = "<tr>\n" . $code . "<td>-$direction_num</td>\n</tr>\n" if $language eq 'arabic';
				$direction_num++;
			} elsif ($section eq 'Image') {
				my ($width, $height) = split(";", $content->{properties});
				my $ID = $content->{imageid};
				my $link = $content->{link};
				$code = "[caption id=\"attachment_$ID\" align=\"aligncenter\" width=\"$width\"]<a href=\"$link\"><img class=\"size-full wp-image-$ID\" src=\"$link\" alt=\"\" width=\"$width\" height=\"$height\" /></a> $text [/caption]";

				# group with directions for easier printing
				$lastImg = "$code<br>\n";
				$lastCaption = $text;

				# if there isnt already a main image, set this one
				if( exists $html{mainImage}{id} && $html{mainImage}{id} ne $ID ) {
					$code .= "<br>\n";
				} else {
					my $align = "dir=\"rtl\"" if $language eq 'arabic';
					$code = "<div style=\"display:none;\"><div id=\"$language$printNum\">\n<h1 $align>$text</h1><br>\n<p $align>www.xawaash.com</p>\n</div></div>\n";
					$html{$language}{printNum}++;
					if ($language eq 'somali') {
						$text = "($text)" if $text;
					}
					$html{mainImage}{dimensions} = $content->{properties};
					$html{mainImage}{id} = $content->{imageid};
					$html{mainImage}{link} = $content->{link};
					$html{mainImage}{text} .= " $text" if $text;
				}
			} elsif ($section eq 'Text') {
				my $style = $content->{properties};
				$style .= $arabic_text_style if $language eq 'arabic' && $text ne '&nbsp;';
				$code = "<span style=\"$style\">$text</span><br>\n";
			}
			$html{$language}{Content} .= $code;
		}
		$html{$language}{Content} .= "</div>\n\n";
	}
	$html{tabs}{Content} = "<div class=\"tabs\">\n<ul>\n" . $html{tabs}{Content} . "</ul>\n\n";
}

sub printScript {
	my $script = "<script type=\"text/javascript\">\nfunction printSelection(language,num){\n";
	my $num = 0;
	my (@list, @list2);
	while ($num < $html{english}{printNum}){
		$script .= "var content$num=document.getElementById(language+'$num').innerHTML\n";
		my $num1 = $num;
		if(exists $images{"content$num"}){ $num1++; $script .= "var content$num1=document.getElementById(language+'$num1').innerHTML\n"; }
		push @list, "content$num1";
		push @list2, "content$num";
		if(exists $images{"content$num"}){ $num++; }
		$num++;
	}
	$script .= "var pwin=window.open('','print_content','width=800,height=500');\n" .
		"var allContent=\"\";\n" .
		"if (num==1) { allContent=" . join('+', @list) . "; }\n" .
		"else { allContent=" . join('+', @list2) . "; }\n" .
		"pwin.document.open();\n" .
		"pwin.document.write('<html><body onload=\"window.print()\">'+allContent+'</body></html>');\n" .
		"pwin.document.close();\n" .
		"setTimeout(function(){pwin.close();},1000);\n" .
		"}</script>\n\n";
	return $script;
}

sub printHTML {
	my $file = shift;
	open RECIPE_OUTPUT, ">", "$file.html";
	binmode(RECIPE_OUTPUT, ":utf8");
	print RECIPE_OUTPUT $html{scripts}{Content};

	# print main image
	my $ID = $html{mainImage}{id};
	my $link = $html{mainImage}{link};
	my ($width, $height) = split(";", $html{mainImage}{dimensions});
	my $text = $html{mainImage}{text};
	my $code = "[caption id=\"attachment_$ID\" align=\"aligncenter\" width=\"$width\"]<a href=\"$link\"><img class=\"size-full wp-image-$ID\" title=\"$text\" src=\"$link\" alt=\"\" width=\"$width\" height=\"$height\" /></a> $text [/caption]\n\n";
	print RECIPE_OUTPUT $code;

	print RECIPE_OUTPUT $html{tabs}{Content};
	foreach my $language (@languages){
		print RECIPE_OUTPUT $html{$language}{Content} if $html{$language}{complete};
	}
	print RECIPE_OUTPUT "</div>\n\n";
	print RECIPE_OUTPUT $html{footer}{Content};
	print RECIPE_OUTPUT printScript();
	close RECIPE_OUTPUT;
	
}

sub main {
	# connect to google spreadsheets
	my $service = Net::Google::Spreadsheets->new(
		username => 'maher@kassims.com',
		password => 'vkmktudgzzrmoinv'
	);

	# read the list of recipes that need to be printed
	my @recipes;
	open FILE, 'recipes.txt';
	while(<FILE>){
		chomp;
		push @recipes, $_ if $_;
	}
	close FILE;
	
	# read the dictionary
	my $ingredient_sheet = $service->spreadsheet({ title => 'Recipe Ingredients' });
	my $content_sheet = $service->spreadsheet({ title => 'Recipe Content' });
	$dictionary = $ingredient_sheet->worksheet({ title => 'Dictionary' });
	foreach my $recipe (@recipes){
		# generate the html for each section
		htmlIngredients($ingredient_sheet->worksheet({ title => $recipe }));
		htmlContent($content_sheet->worksheet({ title => $recipe }));

		#print the html file
		my $file_name = join("_", split(" ", $recipe));
		printHTML($file_name);
	}
}

main();
