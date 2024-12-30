import {PartialType} from "@nestjs/swagger";
import {AlbumDto} from "./album.dto";

export class UpdateAlbumDto extends PartialType(AlbumDto){}
