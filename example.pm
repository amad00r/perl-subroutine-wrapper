package example;

@EXPORT_OK = qw ( conv_hexstring_to_string join parse_parameters error );


sub conv_hexstring_to_string {
    my ($hexstr)=@_;
    if ($hexstr eq "") { return }
    my $tmp=$hexstr;                         
    $tmp =~ s/\s0\d//g;
    $tmp =~ s/[\"\s]+//g;
    if ($tmp =~ /^([A-F0-9]{5,100})/) { 
        $hexstr=$1;
        $hexstr =~ s/([A-F0-9][A-F0-9])/pack("C",hex($1))/eg;
    }
    return $hexstr;
}


sub join {
    my ($list1, $list2)=@_;
    my @list3;
    push @list3, @$list1;
    push @list3, @$list2;
    print "Joined :)";
    return @list3;
}


sub parse_parameters {
    my (@m)=@_;
    my %params;
    for (my $n=0; $n<scalar @m; $n++) {
        if (@m[$n] =~ /^\-(\w+)/ ) {
            my $key=$1;
            if (@m[$n+1] !~ /^\-(\w+)/ ) {
                $params{$key}=@m[++$n]
            } else { 
                $params{$key}="" 
            }
        } else { 
            $params{@m[$n]}="" 
        }
    }
    return %params;
}


sub error {
    warn "This is an error.";
}
