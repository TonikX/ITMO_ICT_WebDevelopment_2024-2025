import {Column, DataType, ForeignKey, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {Artist} from "../artists/artists.model";
import {Album} from "./albums.model";

@Table({tableName: 'album_artists', updatedAt: false})
export class AlbumArtists extends Model<AlbumArtists> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ForeignKey(() => Album)
    @Column({type: DataType.INTEGER})
    albumId: number

    @ForeignKey(() => Artist)
    @Column({type: DataType.INTEGER})
    artistId: number
}